from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class GenericService(models.Model):
    user = models.ForeignKey(User, related_name='services')
    enabled = models.BooleanField(default=True)
    short_name = models.TextField(null=False, max_length=16)
    pretty_name = models.TextField(max_length=80)
    last_poll_time = models.DateTimeField(null=True)


class TumblrService(GenericService):
    tumblr_base_hostname = models.TextField(null=False, max_length=32)
    # oauth_shared_secret = models.TextField(null=True, max_length=128)
    # oauth_token = models.TextField(null=True, max_length=128)


admin.site.register(TumblrService)

