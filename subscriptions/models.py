import base64
import uuid
import random
from datetime import datetime

from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.query_utils import Q
from django.template.loader import render_to_string

import pytz
from sanetime import time, delta
#from sanetime.dj import SaneTimeField
from timezone_field import TimeZoneField

from pytumblr import TumblrRestClient


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
    
    def format_content(self, content):
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
    language = CharField(default='en-us', max_length=12)
    temperature = CharField(default='F', max_length=1)

    dailywakeup_hour = models.IntegerField(null=True)       # for human use; requested local delivery hour
    dailywakeup_bucket = models.IntegerField(null=True,
                                             help_text="""Which bucket this user's dailywakeup should run for. 
                                                         NULL means no daily wakeup.  This should be 90 minutes 
                                                         before the actual daily_wakeup_hour."""
                                             )
    morning_bucket = models.IntegerField(null=True,
                                         help_text="When to run the first content pull/push for the day.")
    evening_bucket = models.IntegerField(null=True,
                                         help_text="When to run the second content pull/push for the day.")
    wee_hours_bucket = models.IntegerField(null=True,
                                         help_text="When to run the third content pull/push for the day.")

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

    @property
    def localnoon_bucket(self, timezone_name='America/Chicago'):
        """
        Given a timezone, figure out local noon.  Convert that to UTC, then
        "bucketize" it, e.g. make it an integer from 0 to 47 where:

        0 = 0:00 - 0:29:59 UTC delivery time
        1 = 0:30 - 0:59:59 UTC delivery time
        2 = 1:00 - 1:29:59 UTC delivery time
        ..
        47 = 23:30 - 23:59:59 UTC delivery time

        Args:
            timezone: string or datetime.timezone maybe?

        Returns:
            int between 0 and 47.  See description.
        """
        timezone = pytz.timezone(timezone_name)
        
        now = time(datetime.now(tz=timezone))
        local_noon = time(now.year, now.month, now.day, 12, 0, 0, 0, now.tz)
        utc_noon = local_noon.set_tz('UTC')
        localnoon_bucket = utc_noon.hour * 2
        if utc_noon.minute:
            localnoon_bucket += 1
        return localnoon_bucket


    def _calculate_dailywakeup_bucket(self, dailywakeup_hour=None):
        """
        Calculates the daily wakeup bucket for this recipient based on the
        Daily Wakeup delivery time specified by the User, and the Recipient's
        time zone.  NOTE that the bucket will be 90 minutes (3 buckets) PRIOR to
        the requested delivery time, because Presto delivery times are approximate
        and their email handling system can be slow.

        Args:
            dailywakeup_hour. int. An hour of the day, 0-23.

        Returns:
            int. The bucket (half-hour division) on the clock during which Daily
                Wakeup content should be aggregated from queue (if any) and dispatched.
                90 minutes before the user's selected delivery time.
        """
        now = time(datetime.now(tz=self.timezone))
        dailywakeup_hour = time(now.year, now.month, now.day, dailywakeup_hour, 0, 0, 0, now.tz)
        dailywakeup_dispatch_delta = delta(m=-90)
        dailywakeup_dispatch_hour = dailywakeup_hour + dailywakeup_dispatch_delta
        return dailywakeup_dispatch_hour.hour * 2


    def set_dailywakeup_bucket(self, delete=False):
		if delete:
			self.dailywakeup_bucket = None
		else:
			self.dailywakeup_bucket = self._calculate_dailywakeup_bucket(self.dailywakeup_hour)

		self.save()


    @staticmethod
    def _calculate_delivery_buckets(localnoon_bucket=36):
        """
        Sets the three basic-user call times:  takes localnoon_bucket
        and returns a morning_bucket (11am), evening_bucket (5pm) and
        wee hours bucket (2am) with an up-to-3-hour shift (in half hour
        aka 1-bucket increments) in either direction away from the given
        times, for local balancing.

        Args:
            localnoon_bucket: int, ranging from 0-47, representing the time in
                UTC which corresponds to the Recipient's local noon.

        Returns:
            tuple of ints. (morning_bucket, evening_bucket, wee_hours_bucket)
                with random shifts applied.
        """
        random.seed()
        morn = random.randint(-6,6)
        eve = random.randint(-6,6)
        weears = random.randint(-6,6)

        morning_bucket = (localnoon_bucket - 2 + morn) % 48
        evening_bucket = (localnoon_bucket + 10 + eve) % 48
        wee_hours_bucket = (localnoon_bucket + 28 + weears) % 48

        return (morning_bucket, evening_bucket, wee_hours_bucket)


    def save(self, *args, **kwargs):
        if self.localnoon_bucket is None:
            self.localnoon_bucket = self._calculate_localnoon_bucket(self.timezone)

        if None in (self.morning_bucket, self.evening_bucket, self.wee_hours_bucket):
            (self.morning_bucket, self.evening_bucket, self.wee_hours_bucket) = \
                self._calculate_delivery_buckets(self.localnoon_bucket)

        return super(Recipient, self).save(*args, **kwargs)


    @staticmethod
    def get_recipients_due_for_processing(bucket):
        """
        Get all of the recipients that are due for a content pull/dispatch.
        Used by manage.py pull_content.
        """
        filters = Q(dailywakeup_bucket=bucket) | Q(morning_bucket=bucket) | Q(evening_bucket=bucket) | Q(wee_hours_bucket=bucket)
        return Recipient.objects.filter(filters)
    
    
    def deliver(self, bucket):
        """
        Run all of the recipient's subscriptions to pull content, format it for presto
        and dispatch it.
        """
        
        for subscription_class in SUBSCRIPTION_CLASSES:
            try:
                #Get all of the recipient's tumblr subs.
                subs = subscription_class.objects.filter(recipient=self)
                for sub in subs:
                    content = sub.pull_content()
                    formatted_content = sub.format_content(content)
                    self.dispatch(formatted_content)
            except subscription_class.DoesNotExist:
                pass #they don't have any of these

        #if the current run also matches the recipient's daily wakeup scheduled time, run it.
        if self.dailywakeup_bucket == bucket:
            try:
                sub = DailyWakeupSubscription.objects.get(recipient=self)
                content = sub.pull_content()
                formatted_content = sub.format_content(content)
                self.dispatch(formatted_content)
            except (DailyWakeupSubscription.DoesNotExist, 
                    DailyWakeupSubscription.MultipleObjectsReturned):
                pass #something's broken, skip it.

    def dispatch(self, content):
        """
        Sends content to this recipient's print queue.
        
        @todo: figure out a standard format for the results of format_content, extract it here to hand off to django's send_mail.
        """
        content = "".join(content)
        subject = "Your Share2Grandma update from plugin_name"
        destination = self.email

        send_mail(subject, content, self.sender.profile.s2g_email,
                  [self.email], fail_silently=False)
        

#class SubscriptionBundle(object):
#    
#    def __init__(self, subscription_name,
#                 contents, date_created, 
#                 destination, sender):
#        
        





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
		self.recipient.set_dailywakeup_bucket()
        
        return super(DailyWakeupSubscription, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
		self.recipient.set_dailywakeup_bucket(delete=True)

		return super(DailyWakeupSubscription, self).delete(*args, **kwargs)
		

    @property
    def timezone(self):
        return self.recipient.timezone
    
    def get_absolute_url(self):
        return reverse('subscription_detail_dailywakeup', kwargs={'pk':self.pk})

    def __unicode__(self):
        # so it's intelligible in the django admin
        return "%s (DailyWakeup) sub for %s" % (self.short_name, self.user)
    
    def pull_content(self):
        """
        Returns content from a daily wakeup subscription.
        
        @todo: read DailyWakeupContent objects for actual content.
        """
        timezone = self.recipient.timezone
        current_time = timezone.localize(datetime.now())
        translation.activate(recipient.language)
        result = render_to_string('subscriptions/email/daily_wakeup.txt', {'now':current_time})
        return result

    def format_content(self, content):
        return content
        

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


#a list of all of the subscription classes, used by deliver() for priority.
#DailyWakeUp is not included and is called manually at the end of deliver().
SUBSCRIPTION_CLASSES = [TumblrSubscription, ]
