from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.urlresolvers import reverse

from .tumblr_subscription_processor import TumblrSubscriptionProcessor

class GenericSubscription(models.Model):
    user = models.ForeignKey(User, related_name='subscriptions')
    enabled = models.BooleanField(default=True)
    short_name = models.CharField(null=False, max_length=16)
    pretty_name = models.CharField(blank=True, max_length=80)
    avatar = models.TextField(null=True, blank=True)      # set to generic for subscriptions w/no avatar


class TumblrSubscription(GenericSubscription):
    last_post_ts = models.BigIntegerField(null=True, blank=True)

    def update_from_tumblr(self, save=False):
        processor = TumblrSubscriptionProcessor(self)
        info = processor.get_blog_info()

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


class TumblrSubscriptionForm(ModelForm):
    class Meta:
        model = TumblrSubscription
        exclude = ('pretty_name', 'avatar', 'last_post_ts')     # user can't twiddle these


admin.site.register(TumblrSubscription)

