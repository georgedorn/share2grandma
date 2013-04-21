from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class GenericService(models.Model):
    user = models.ForeignKey(User, related_name='services')
    enabled = models.BooleanField(default=True)
    short_name = models.TextField(null=False, max_length=16)
    pretty_name = models.TextField(max_length=80)
    last_post_ts = models.BigIntegerField(null=True, blank=True)
    avatar = models.StringField(null=True, blank=True)      # set to generic for services w/no avatar


class TumblrService(GenericService):
    tumblr_base_hostname = models.TextField(null=False, max_length=255)


admin.site.register(TumblrService)

