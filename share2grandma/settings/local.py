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
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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

#These tumblr keys point to a demo app.  It redirects to localhost:8000.  Use in dev mode.
TUMBLR_CONSUMER_KEY = 'PsbqraXHdjAOpHf31vJ7fa4UIyUTeRwVlX3AxUOmtwqHQWZgbh'
TUMBLR_API_KEY = TUMBLR_CONSUMER_KEY
TUMBLR_CONSUMER_SECRET = 'C1P3TznBoZsNtrfAxnQSoWLDSq0J6Msnk468OJfTMF90XOipbO'

#These google keys point to a demo app.  Redirects to localhost:8000.
GOOGLE_OAUTH2_CLIENT_ID = '203401500199-mmi2uonvq09ksnspjj8ofbt6gdi8upch.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'sijcp1Uyx5l1O1vKTFEYij3x'

