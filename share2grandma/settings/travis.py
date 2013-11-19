"""
Settings file for running Travis-CI tests.

Use me with:
export DJANGO_SETTINGS_MODULE="share2grandma.settings.travis"

Or:
django-admin.py --settings="share2grandma.settings.travis" yourcommandhere
"""

from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

DB_TYPE = os.getenv('DB')


if DB_TYPE == 'sqlite':
    DATABASES = {
                 "default": {
                             "ENGINE": "django.db.backends.sqlite3",
                             "NAME": "share2grandma.db",
                             }
                 }
elif DB_TYPE == 'postgresql':
    DATABASES = {
                 "default": {
                             "ENGINE": "django.db.backends.postgresql_psycopg2",
                             "NAME": "s2g",
                             "USER": "postgres"
                             }
                 }

TUMBLR_CONSUMER_KEY = 'PsbqraXHdjAOpHf31vJ7fa4UIyUTeRwVlX3AxUOmtwqHQWZgbh'
TUMBLR_CONSUMER_SECRET = 'C1P3TznBoZsNtrfAxnQSoWLDSq0J6Msnk468OJfTMF90XOipbO'
TUMBLR_API_KEY = TUMBLR_CONSUMER_KEY

