"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .views import AUTH_SERVICES
from social_auth.models import SOCIAL_AUTH_MODELS_MODULE
UserSocialAuth = SOCIAL_AUTH_MODELS_MODULE.UserSocialAuth


class TestAccountAuthServices(TestCase):

    def setUp(self):
        self.auth_list_url = reverse('auth_services_list')
        self.userdata = {'username':'xenuuu',
                         'password':'test_pass'}
        self.user = User.objects.create_user(**self.userdata)
    
    def test_logged_in_s2g(self):
        self.client.login(**self.userdata)
        
        res = self.client.get(self.auth_list_url)
        
        #we're logged in with s2g but nothing else, so all of the other services
        #should present login links
        for key in AUTH_SERVICES:
            if key == 's2g':
                continue
            
            auth_begin_url = reverse('socialauth_begin', kwargs={'backend':key})
            self.assertTrue(auth_begin_url in res.content)
            

    def test_logged_in_tumblr(self):
        """
        Fake being logged in via tumlbr, then check the auth list.
        """
        UserSocialAuth.objects.create(user=self.user,
                                      provider='tumblr',
                                      uid='monkey')
        self.client.login(**self.userdata)
        res = self.client.get(self.auth_list_url)

        #so, at this point the user is logged in with s2g and tumblr (can't actually test just tumblr due to django-social-auth's limitations)
        for key in AUTH_SERVICES:
            if key == 'tumblr':
                expected_url = reverse('socialauth_disconnect', kwargs={'backend':key})
            elif key == 's2g':
                expected_url = reverse('django.contrib.auth.views.logout')
            else:
                expected_url = reverse('socialauth_begin', kwargs={'backend':key})
            
            self.assertTrue(expected_url in res.content)