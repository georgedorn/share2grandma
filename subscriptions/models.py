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
    # @todo wakeup / postcode field here - https://github.com/mthornhill/django-postal -- for DailyWakeup weather

    def get_absolute_url(self):
        return reverse('recipient_detail', kwargs={'pk':self.pk})

    def is_on_vacation(self):
        now = timezone.now()
        return Vacation.objects.filter(start_date__lt=now,
                                       end_date__gt=now,
                                       recipient=self).exists()


class TumblrSubscription(GenericSubscription):
    last_post_ts = models.BigIntegerField(null=True, blank=True)

    def update_from_tumblr(self, save=False):
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
    user = models.OneToOneField(User)
    __s2g_email = models.EmailField(null=True)

    @property
    def s2g_email(self):
        """
        returns a static s2g email from self.__s2g_email or generates,
        saves, then returns it if it doesn't exist.
        """
        if self.__s2g_email is None:
            generated_okay = False

            while not generated_okay:
                u = uuid.uuid4()        # random
                u = u.fields['node']    # 48 bits = 8 b64 chars
                suffix = base64.b64encode(str(u), '-_')
                email = "s2g%s" % suffix

                if Profile.objects.count(__s2g_email=email) == 0:
                    self.__s2g_email = email
                    self.save()
                    generated_okay = True

        return self.__s2g_email
