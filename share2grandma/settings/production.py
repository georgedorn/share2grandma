"""
Production settings.  Requires various env vars to be set.
"""
import os
from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Devs', 'devs@share2grandma.com'),)

ALLOWED_HOSTS = [
                'app.share2grandma.com',
                'taffy.utopiadammit.com' #remove me when this is fixed

]

#todo:  figure this out
#EMAIL_HOST = "localhost"
#EMAIL_PORT = 1025

DB_USER = 's2g'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 's2g',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': DB_USER,
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

#These MUST be set in the environment or kaboom.
SECRET_KEY = os.environ['SECRET_KEY']
TUMBLR_CONSUMER_KEY = os.environ['TUMBLR_CONSUMER_KEY']
TUMBLR_API_KEY = TUMBLR_CONSUMER_KEY
TUMBLR_CONSUMER_SECRET = os.environ['TUMBLR_CONSUMER_SECRET']
GOOGLE_OAUTH2_CLIENT_ID = os.environ['GOOGLE_OAUTH2_CLIENT_ID']
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ['GOOGLE_OAUTH2_CLIENT_SECRET']
