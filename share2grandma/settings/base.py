# Django settings for share2grandma project.

import os
from os import getenv
from django.utils.translation import ugettext_lazy as _

SETTINGS_PATH = os.path.dirname(__file__)
PROJECT_PATH = os.path.dirname(SETTINGS_PATH)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# MANAGERS, ADMINS, DATABASES in local_settings.py


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

#Available languages.  See https://docs.djangoproject.com/en/1.5/topics/i18n/translation/
LANGUAGES = [
			  ('es', _('European Spanish')),
			  ('es-mx', _('Mexican Spanish')),
			  ('en-us', _('American English')),
			  ('en-gb', _('British English')),
			]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

DATE_FORMAT = "Y-m-d"

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media_root') 

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/' 

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static_root') 

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'static_media'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ejq)i8^su3bvz*b-+x8^9v(2o!ge2i6%@y4(0r8@bm_&sbve1a'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROESSORS = (
    'django.core.context_processors.request',   # django-socialregistration
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',   # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'share2grandma.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'share2grandma.wsgi.application'



TEMPLATE_DIRS = (
                 os.path.join(PROJECT_PATH, 'templates'), #share2grandma/templates/
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    ### 3rd party
    'django.contrib.sites',
    'accounts',
    'social_auth',
    'south',
    'registration',
    ### our stuff
    'dashboard',
    'subscriptions',
    'dispatch',
    'project_tests', #just tests, no models
)

AUTHENTICATION_BACKENDS = (
                          'social_auth.backends.contrib.tumblr.TumblrBackend', 
#    'social_auth.backends.twitter.TwitterBackend',
#    'social_auth.backends.facebook.FacebookBackend',
#    'social_auth.backends.google.GoogleOAuthBackend',
                          'social_auth.backends.google.GoogleOAuth2Backend',
#    'social_auth.backends.google.GoogleBackend',
#    'social_auth.backends.yahoo.YahooBackend',
#    'social_auth.backends.browserid.BrowserIDBackend',
#    'social_auth.backends.contrib.linkedin.LinkedinBackend',
#    'social_auth.backends.contrib.disqus.DisqusBackend',
#    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
#    'social_auth.backends.contrib.orkut.OrkutBackend',
#    'social_auth.backends.contrib.foursquare.FoursquareBackend',
#    'social_auth.backends.contrib.github.GithubBackend',
#    'social_auth.backends.contrib.vk.VKOAuth2Backend',
#    'social_auth.backends.contrib.live.LiveBackend',
#    'social_auth.backends.contrib.skyrock.SkyrockBackend',
#    'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
#    'social_auth.backends.contrib.readability.ReadabilityBackend',
#    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)


AUTH_PROFILE_MODULE = 'subscriptions.Profile'


#Until this bug is in the next django release, don't change the LOGIN_URL.
#https://code.djangoproject.com/ticket/20114
LOGIN_URL          = '/registration/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_ERROR_URL    = '/login-error/'

ACCOUNT_ACTIVATION_DAYS = 7 #how long you have to verify your account before it's nuked
SOCIAL_AUTH_FORCE_POST_DISCONNECT = True

TUMBLR_CONSUMER_KEY = getenv('TUMBLR_CONSUMER_KEY')
TUMBLR_API_KEY = TUMBLR_CONSUMER_KEY
TUMBLR_CONSUMER_SECRET = getenv('TUMBLR_CONSUMER_SECRET')

GOOGLE_OAUTH2_CLIENT_ID = getenv('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = getenv('GOOGLE_OAUTH2_CLIENT_SECRET')

#Don't run these social auth tests:
SOCIAL_AUTH_TEST_TWITTER = False
SOCIAL_AUTH_TEST_FACEBOOK = False
SOCIAL_AUTH_TEST_GOOGLE = False
SOCIAL_AUTH_TEST_ODNOKLASSNIKI = False

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


TUMBLR_API_KEY = os.environ.get('TUMBLR_API_KEY')


#Testing-related
TEST_RUNNER = 'share2grandma.test_runner.AppTestSuiteRunner'
TEST_IGNORE_APPS = ('django_extensions',)




