"""
Production settings.  Requires various env vars to be set.
"""
import os
from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

#todo:  figure this out
#EMAIL_HOST = "localhost"
#EMAIL_PORT = 1025

DB_USER = 'grandma_app_user'
DB_PASS = os.environ['DB_PASS']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'grandma_app_db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5433',                      # Set to empty string for default.
    }
}


