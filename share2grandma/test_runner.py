from django.test.simple import DjangoTestSuiteRunner, build_suite
from django.conf import settings
from django.db.models.loading import get_apps
from django.utils import unittest

class AppTestSuiteRunner(DjangoTestSuiteRunner):
    """
    A test runner that doesn't run tests for apps in settings.TEST_IGNORE_APPS.
    
    See http://www.mavenrd.com/blog/django-testing-unchained/
    """
    def build_suite(self, test_labels, *args, **kwargs):
        if test_labels:
            return super(AppTestSuiteRunner, self).build_suite(test_labels, *args, **kwargs)
        else:
            ignore_apps = getattr(settings, 'TEST_IGNORE_APPS', None)
            if not ignore_apps: #we don't have this set, so just do normal behavior
                return super(AppTestSuiteRunner, self).build_suite(test_labels, *args, **kwargs)

            print "Ignoring tests matching these apps: %s" % ignore_apps
            #if we're here, we have a list of apps to ignore, and will have to build the suite ourselves
            suite = unittest.TestSuite()
            for app in get_apps():
                app_name = app.__name__
                if app_name.endswith('.models'):
                    app_name = app_name[0:-7]
                if app_name not in ignore_apps:
                    print "Running %s's tests" % app_name
                    suite.addTest(build_suite(app))
                else:
                    print "Skipping %s's tests" % app_name
            return suite