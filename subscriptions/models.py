from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from .tumblr_service_processor import TumblrSubscriptionProcessor

class GenericSubscription(models.Model):
    user = models.ForeignKey(User, related_name='services')
    enabled = models.BooleanField(default=True)
    short_name = models.TextField(null=False, max_length=16)
    pretty_name = models.TextField(null=True, blank=True, max_length=80)
    avatar = models.TextField(null=True, blank=True)      # set to generic for services w/no avatar


class TumblrSubscription(GenericSubscription):
    last_post_ts = models.BigIntegerField(null=True, blank=True)


    def __init__(self, *args, **kwargs):
        # call update_from_tumblr here... sometimes?
        super(TumblrSubscription, self).__init__(*args, **kwargs)


    def update_from_tumblr(self, save=False):
        processor = TumblrSubscriptionProcessor(self)
        info = processor.get_blog_info()

        self.avatar = info['avatar']
        self.pretty_name = info['pretty_name']
        self.last_post_ts = info['last_post_ts']

        if save is True:
            self.save()


admin.site.register(TumblrSubscription)

