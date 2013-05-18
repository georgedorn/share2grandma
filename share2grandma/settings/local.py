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
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

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

TUMBLR_CONSUMER_KEY = 'PsbqraXHdjAOpHf31vJ7fa4UIyUTeRwVlX3AxUOmtwqHQWZgbh'
TUMBLR_API_KEY = TUMBLR_CONSUMER_KEY
TUMBLR_CONSUMER_SECRET = 'C1P3TznBoZsNtrfAxnQSoWLDSq0J6Msnk468OJfTMF90XOipbO'

