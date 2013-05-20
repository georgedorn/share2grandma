"""
Tests of account creation/management.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator


from social_auth.backends import get_backends
from registration.models import RegistrationProfile
from django.utils.http import int_to_base36
from django.contrib.auth.forms import SetPasswordForm

User = get_user_model()

#dummy
#from django.contrib.auth.models import User

class RegistrationTestCase(TestCase):
    
    def setUp(self):
        """
        Get the urls we are going to use.
        """
        self.login_url = reverse('auth_login')
        self.reset_password_url = reverse('auth_password_reset')
        self.create_account_url = reverse('registration_register')
        self.change_password_url = reverse('auth_password_change')
        
        self.login_redirect_url = settings.LOGIN_REDIRECT_URL

        self.social_auth_backends = get_backends()
        social_auth_names = self.social_auth_backends.keys()
        
        self.social_auth_login_urls = [reverse('socialauth_begin', kwargs={'backend':backend}) 
                                        for backend in social_auth_names]
        
        import IPython
        self.shell = IPython.embed
    
    
    def test_login_form_exists(self):
        """
        Given a user, log in via the client.
        """
        res = self.client.get(self.login_url)
        
        #should see password reset, login_url, and the social auth login urls
        for social_auth_login_url in self.social_auth_login_urls:
            self.assertTrue(social_auth_login_url in res.content)
        
        self.assertTrue(self.login_url in res.content)
        self.assertTrue(self.reset_password_url in res.content)
        self.assertTrue(self.create_account_url in res.content)


    def test_login_form_works(self):
        data = {'username':'test_user',
                'password':'test_pass'}
        User.objects.create_user(**data)
        
        res = self.client.post(self.login_url, data)

        #should redirect to wherever LOGIN_REDIRECT_URL says
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['Location'], 'http://testserver%s' % self.login_redirect_url)
        
    def test_bad_login(self):
        User.objects.create_user(username='monkey',
                                 password='good_password')
        data = {'username': 'monkey',
                'password': 'bad_password'}
        
        res = self.client.post(self.login_url, data)
        
        self.assertEqual(res.status_code, 200) #a bad login just re-GETs the form, not an http auth error
        
        form = res.context_data['form']
        self.assertTrue(form.non_field_errors()) #not testing the message, just that it didn't work

    def test_registration(self):
        data = {'username':'test_monkey',
                'password1':'test_monkey_pass',
                'password2':'test_monkey_pass',
                'email':'test_monkey@testuser.org'}
        
        res = self.client.post(self.create_account_url, data, follow=True)

        #should have created a user
        user = User.objects.get(username='test_monkey')
        
        #but user is not active
        self.assertFalse(user.is_active)

    def test_complete_registration(self):
        user = User.objects.create_user(username='test_monkey',
                                        password='test_pass')
        user.is_active = False
        
        profile = RegistrationProfile.objects.create(activation_key='aoeu',
                                                     user=user)
        
        registration_complete_url = reverse('registration_activate', 
                                            kwargs={'activation_key': profile.activation_key})
        
        res = self.client.get(registration_complete_url)
        
        user = User.objects.get(pk=user.pk) #reload user
        self.assertTrue(user.is_active)
        
    def test_reset_password_form(self):
        user = User.objects.create_user(username='test_monkey',
                                        password='test_pass', 
                                        email='test_monkey@email.org')

        data = {'email':user.email}        
        res = self.client.post(self.reset_password_url, data, follow=True)
        
        email = mail.outbox[0]
        self.assertEqual(email.to, [user.email])
        self.assertTrue(user.username in email.body)
        confirm_url = self._get_confirm_url(user)
        
        self.assertTrue(confirm_url in email.body)

    def _get_confirm_url(self, user):
        token_maker = PasswordResetTokenGenerator()
        token = token_maker.make_token(user)
        uid = int_to_base36(user.pk) #dunno, something auth does
        confirm_url = reverse('auth_password_reset_confirm', 
                              kwargs={'token':token,
                                      'uidb36':uid})
        return confirm_url

    def test_reset_password(self):
        user = User.objects.create_user(username='test_monkey',
                                        password='test_pass', 
                                        email='test_monkey@email.org')

        confirm_url = self._get_confirm_url(user)
        res = self.client.get(confirm_url)
        
        #we should be at the password change form
        context = res.context_data
        self.assertTrue(context['validlink'])
        self.assertTrue(isinstance(context['form'], SetPasswordForm))

        #this is bad form, but we're already here, let's finish the process
        data = {'new_password1':'aoeu',
                'new_password2':'aoeu'}
        res = self.client.post(confirm_url, data)
        
        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.check_password('aoeu'))
