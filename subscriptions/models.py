import base64
import uuid

from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from timezone_field import TimeZoneField

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from pytumblr import TumblrRestClient
from django.conf import settings
from django.db.models.query_utils import Q


class GenericSubscription(models.Model):
    recipient = models.ForeignKey('Recipient', related_name='subscriptions')
    enabled = models.BooleanField(default=True)
    short_name = models.CharField(null=False, max_length=16)
    pretty_name = models.CharField(blank=True, max_length=80)
    avatar = models.TextField(null=True, blank=True)      # set to generic for subscriptions w/no avatar

    num_borked_calls = models.IntegerField(null=False, default=0)    # how many times in a row we had a borked call?
    first_borked_call_time = models.DateTimeField(null=True)            # and since when?
    appears_broken = models.BooleanField(default=False)                 # are we pretty sure user intervention is needed?

    def pull_content(self):
        raise NotImplementedError

    def pull_metadata(self):
        raise NotImplementedError
    

class Recipient(models.Model):
    sender = models.ForeignKey(User, related_name='recipients')
    # the following can differ per recipient.  "bobby" vs "Robert" etc.
    sender_name = models.CharField(null=False, blank=False, max_length=64)
    # also variable by recipient
    sender_phone = models.CharField(null=False, blank=False, max_length=20)
    name = models.CharField(null=False, blank=False, max_length=64)
    add_date = models.DateField(auto_now_add=True)
    email = models.EmailField(null=False, blank=False)
    timezone = TimeZoneField(default='America/Los_Angeles')
    
    bucket = models.IntegerField(null=True)
    # For weather with DailyWakeup ... @todo
    # city
    # state
    # country - django-countries?
    postcode = models.CharField(null=True, blank=True, max_length=16)

    def get_absolute_url(self):
        return reverse('recipient_detail', kwargs={'pk':self.pk})

    def is_on_vacation(self):
        if self.get_current_vacation():
            return True
        return False
    
    def get_current_vacation(self):
        now = timezone.now()
        vacations = Vacation.objects.filter(start_date__lt=now,
                                       end_date__gt=now,
                                       recipient=self)
        if vacations:
            return vacations[0]
        return None
    
    def get_upcoming_vacations(self):
        now = timezone.now()
        return Vacation.objects.filter(start_date__gt=now,
                                       recipient=self).order_by('start_date')

    @staticmethod
    def get_vacationing_recipients():
        """
        Returns a queryset of recipients currently on vacation, for 
        exclusion from processing.
        """
        now = timezone.now()
        return Recipient.objects.filter(vacations__start_date__lt=now,
                                        vacations__end_date__gt=now).distinct()
        
    def save(self, *args, **kwargs):
        if self.bucket is None:
            #@todo: hash primary key into X buckets for load balancing
            self.bucket = 1
        return super(Recipient, self).save(*args, **kwargs)
    
    @staticmethod
    def get_recipients_due_for_pull(bucket, daily_wakeup_bucket=None):
        """
        Get all of the recipients that are due for a content pull.
        Used by manage.py pull_content.
        """
        if daily_wakeup_bucket is not None:
            wakeups = DailyWakeupSubscription.objects.filter(delivery_bucket=daily_wakeup_bucket)
            wakeup_recipient_ids = [wakeup.recipient.pk for wakeup in wakeups]
            filters = Q(bucket=bucket) | Q(pk__in=wakeup_recipient_ids)
        else:
            filters = Q(bucket=bucket)

        return Recipient.objects.filter(filters)



class TumblrSubscription(GenericSubscription):
    last_post_ts = models.BigIntegerField(null=True, blank=True)

    def _make_client(self):
        """
        Creates a tumblr client and read the blog's info to
        verify it exists and gets metadata.
        """
        client = TumblrRestClient(consumer_key=settings.TUMBLR_API_KEY)
        blog_info_raw = client.blog_info(self.short_name)

        if 'meta' in blog_info_raw.keys():
            e_msg = "Status %s - %s" % (blog_info_raw['meta']['status'], blog_info_raw['meta']['msg'])
            if int(blog_info_raw['meta']['status']) == 404:
                raise KeyError, e_msg
            else:
                raise ValueError, e_msg

        client.tumblr_info = blog_info_raw['blog']
        return client

    def pull_content(self):
        """
        Get new blog entries from tumblr.
        """
        client = self._make_client()
        post_list = []

        # Step 1: check if updated, if not, don't start pulling posts and bail early
        if(client.tumblr_info['updated'] <= self.last_post_ts):
            return post_list
        
        # Step 2: Repeatedly get posts from blog 
        done_queueing = False

        while not done_queueing:
            twenty_posts = self.client.posts(self.short_name,
                                             limit=20,
                                             offset=len(post_list))['posts']

            for post in twenty_posts:
                # Step 3: and stop when we see one <= self.subscription.last_poll_time

                if post['timestamp'] <= self.last_post_ts:
                    done_queueing = True #checked by while loop
                    break
                else:
                    self.tumblr_post_list.append(post)

        return post_list

    
    def pull_metadata(self, save=False):
        """
        Get info about the blog from Tumblr; not the content.
        """
        client = self._make_client()
        
        # Get avatar
        self.avatar = client.avatar(self.short_name)['avatar_url']

        # Get blog pretty_name
        self.pretty_name = client.tumblr_info['title']

        # Get most recent post's timestamp
        self.last_post_ts = client.tumblr_info['updated']

        if save is True:
            self.save()

    def save(self, *args, **kwargs):
        # check if it looks like this is a brand new object, if so, pull the
        # data from tumblr
        if not self.avatar and not self.pretty_name:
            self.pull_metadata()

        super(TumblrSubscription, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('subscription_detail_tumblr', kwargs={'pk':self.pk})

    def __unicode__(self):
        # so it's intelligible in the django admin
        return "%s (Tumblr) sub for %s" % (self.short_name, self.user)

admin.site.register(TumblrSubscription)


class DailyWakeupSubscription(GenericSubscription):
    delivery_time = models.IntegerField() #hour, from 0-23, in recipient's timezone
    delivery_bucket = models.IntegerField() #hour, from 0-23, in UTC
    
    def save(self, *args, **kwargs):
        #@todo: calculate delivery_bucket based on the delivery time and recipient's timezone
        
        return super(DailyWakeupSubscription, self).save(*args, **kwargs)
    
        
    @property
    def timezone(self):
        return self.recipient.timezone
    
    def get_absolute_url(self):
        return reverse('subscription_detail_dailywakeup', kwargs={'pk':self.pk})

    def __unicode__(self):
        # so it's intelligible in the django admin
        return "%s (DailyWakeup) sub for %s" % (self.short_name, self.user)

admin.site.register(DailyWakeupSubscription)


class DailyWakeupContent(models.Model):
    expires = models.DateTimeField()
    daily_wakeup_subscription = models.ForeignKey(DailyWakeupSubscription)
    content = models.CharField(max_length=160)
    
    subscription_type = models.ForeignKey(ContentType) #which subscription class provided this content?  e.g. tumblr, gcal
    subscription_id = models.PositiveIntegerField() #which instance of the subscription class provided this content?  e.g. Bob's gcal subscriptions, Annie's tumblr
    content_source = generic.GenericForeignKey('subscription_type', 'subscription_id')


class Vacation(models.Model):
    recipient = models.ForeignKey(Recipient, related_name='vacations')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        """
        Last-ditch effort to ensure that start/end dates have the right timezones,
        namely that of their recipients.
        """
        if timezone.is_naive(self.start_date):
            self.start_date = timezone.make_aware(self.start_date, self.recipient.timezone)
        if timezone.is_naive(self.end_date):
            self.end_date = timezone.make_aware(self.end_date, self.recipient.timezone)
        return super(Vacation, self).save(*args, **kwargs)


# @todo a lot of random shit is getting dumped into subscriptions.models....
class Profile(models.Model):
    """
    Extend User with moar information.
    """
    user = models.OneToOneField(User, related_name='s2g_profile')
    s2g_email = models.EmailField(null=True)

    def save(self, *args, **kwargs):
        """
        On save, if this object doesn't have a proper s2g_email, we generate
        one randomly.
        """
        if self.s2g_email is None:
            generated_okay = False

            while not generated_okay:
                u = str(uuid.uuid4())[-8:]        # 8 random chars
                email = "s2g_%s" % u

                if not Profile.objects.filter(s2g_email=email).exists():
                    self.s2g_email = email
                    generated_okay = True

        return super(Profile, self).save(*args, **kwargs)

# http://stackoverflow.com/questions/13460426/get-user-profile-in-django
# http://stackoverflow.com/a/10575330/402605 (don't create superuser during syncdb)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)
