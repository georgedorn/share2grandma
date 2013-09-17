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

# Maybe???
# SOUTH_TESTS_MIGRATE = bool(os.environ.get('SOUTH_TESTS_MIGRATE', True))
# SKIP_SOUTH_TESTS = os.environ.get('SKIP_SOUTH_TESTS', True)

#These tumblr keys point to a demo app.  It redirects to localhost:8000.  Use in dev mode.
TUMBLR_CONSUMER_KEY = 'PsbqraXHdjAOpHf31vJ7fa4UIyUTeRwVlX3AxUOmtwqHQWZgbh'
TUMBLR_API_KEY = TUMBLR_CONSUMER_KEY
TUMBLR_CONSUMER_SECRET = 'C1P3TznBoZsNtrfAxnQSoWLDSq0J6Msnk468OJfTMF90XOipbO'

#These google keys point to a demo app.  Redirects to localhost:8000.
GOOGLE_OAUTH2_CLIENT_ID = '203401500199-mmi2uonvq09ksnspjj8ofbt6gdi8upch.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'sijcp1Uyx5l1O1vKTFEYij3x'

INSTALLED_APPS += ('django_extensions','debug_toolbar')

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)


#Debug toolbar stuff.  If we're using local.py, we want the toolbar.  Nevermind the IP address nonsense.
def custom_show_toolbar(request):
    if request.META['SERVER_NAME'] == 'testserver':
        return False #don't show debug in html output when running tests
    return True  # Always show toolbar, for example purposes only.

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'ENABLE_STACKTRACES' : True,
}

