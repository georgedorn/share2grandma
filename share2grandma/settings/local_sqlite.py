"""
Override for settings.local to allow use of sqlite dbs.
Don't use if you can possibly avoid it.
"""

from .local import *

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
