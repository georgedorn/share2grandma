"""
Settings file for local dev against sqlite3.  For now.

Use me with:
export DJANGO_SETTINGS_MODULE="share2grandma.settings.local"

Or:
django-admin.py --settings="share2grandma.settings.local" yourcommandhere
"""

from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

DATABASES = {
             "default": {
                         "ENGINE": "django.db.backends.sqlite3",
                         "NAME": "share2grandma.db",
                         "USER": "",
                         "PASSWORD": "",
                         "HOST": "localhost",
                         "PORT": "",
                         }
             }
