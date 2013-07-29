import base64
import uuid

from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from timezone_field import TimeZoneField

from .tumblr_subscription_processor import TumblrSubscriptionProcessor


class GenericSubscription(models.Model):
    recipient = models.ForeignKey('Recipient', related_name='subscriptions')
    enabled = models.BooleanField(default=True)
    short_name = models.CharField(null=False, max_length=16)
    pretty_name = models.CharField(blank=True, max_length=80)
    avatar = models.TextField(null=True, blank=True)      # set to generic for subscriptions w/no avatar

    num_borked_calls = models.IntegerField(null=False, default=0)    # how many times in a row we had a borked call?
    first_borked_call_time = models.DateTimeField(null=True)            # and since when?
    appears_broken = models.BooleanField(default=False)                 # are we pretty sure user intervention is needed?


class Recipient(models.Model):
    user = models.ForeignKey(User, related_name='recipients')
    # the following can differ per recipient.  "bobby" vs "Robert" etc.
    sender_name = models.CharField(null=False, blank=False, max_length=64)
    # also variable by recipient
    sender_phone = models.CharField(null=False, blank=False, max_length=20)
    name = models.CharField(null=False, blank=False, max_length=64)
    add_date = models.DateField(auto_now_add=True)
    email = models.EmailField(null=False, blank=False)
    timezone = TimeZoneField(default='America/Los_Angeles')
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


class TumblrSubscription(GenericSubscription):
    last_post_ts = models.BigIntegerField(null=True, blank=True)

    def update_from_tumblr(self, save=False):
        """
        @todo this should probably be named something that doesn't imply that it's
        updating *content*, because it isn't.
        """
        processor = TumblrSubscriptionProcessor(self)
        info = processor.setup_subscription()

        self.avatar = info['avatar']
        self.pretty_name = info['pretty_name']
        self.last_post_ts = info['last_post_ts']

        if save is True:
            self.save()

    def save(self, *args, **kwargs):
        # check if it looks like this is a brand new object, if so, pull the
        # data from tumblr
        if not self.avatar and not self.pretty_name:
            self.update_from_tumblr()

        super(TumblrSubscription, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('subscription_detail_tumblr', kwargs={'pk':self.pk})

    def __unicode__(self):
        # so it's intelligible in the django admin
        return "%s (Tumblr) sub for %s" % (self.short_name, self.user)

admin.site.register(TumblrSubscription)


class DailyWakeupSubscription(GenericSubscription):
    def get_absolute_url(self):
        return reverse('subscription_detail_dailywakeup', kwargs={'pk':self.pk})

    def __unicode__(self):
        # so it's intelligible in the django admin
        return "%s (DailyWakeup) sub for %s" % (self.short_name, self.user)

admin.site.register(DailyWakeupSubscription)


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
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)
