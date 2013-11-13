"""
General tests of all of the major urls, both logged-in and not.

Really only checks for 200s, login redirects and 400s.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.models import User
from subscriptions.models import Recipient, TumblrSubscription, Vacation
from sanetime import time, delta

class ViewsTests(TestCase):
    
    def setUp(self):
        self.userdata = {'username':'xenuuu',
                         'password':'test_pass'}

        self.user = User.objects.create_user(**self.userdata)
        self.user = User.objects.get_by_natural_key('xenuuu')
        
        self.recipient = Recipient.objects.create(sender=self.user,
                                                  sender_name='bob',
                                                  sender_phone='000-000-0000',
                                                  name='granny',
                                                  email='bob@yruncle.com'
                                                )
        self.subscription = TumblrSubscription.objects.create(recipient=self.recipient,
                                                              short_name='bobs_monkeys',
                                                              pretty_name="Bob's Monkey Photos",
                                                              avatar='monkey.jpg') #supplying all fields to avoid call to tumblr

        start_dt = time() - delta(hours=1 * 7 * 24)
        end_dt = time() + delta(hours=1 * 7 * 24)
        self.vacation = Vacation.objects.create(recipient=self.recipient,
                                                start_date=start_dt.datetime,
                                                end_date=end_dt.datetime
                                                )

        #urls of things that require you to be logged in to access        
        self.login_required_urls = [
                               reverse_lazy('subscription_create_tumblr'),
                               reverse_lazy('subscription_list'),
                               reverse_lazy('subscription_detail_tumblr', kwargs={'pk':self.subscription.pk}),
                               reverse_lazy('subscription_delete_tumblr', kwargs={'pk':self.subscription.pk}),
                               reverse_lazy('recipient_create'),
                               reverse_lazy('recipient_detail', kwargs={'pk':self.recipient.pk}),
                               reverse_lazy('vacation_create', kwargs={'recipient_id':self.recipient.pk}),
                               reverse_lazy('vacation_cancel', kwargs={'pk':self.vacation.pk})

                               #todo:  delete the recipient
                       
                       ]
        
        #urls of things that you must own the object in question (or a related one) in order to access.
        #these will just be tested by being logged in as a user other than xenuuu
        self.ownership_required_urls = [
                               reverse_lazy('subscription_detail_tumblr', kwargs={'pk':self.subscription.pk}),
                               reverse_lazy('subscription_delete_tumblr', kwargs={'pk':self.subscription.pk}),
                               reverse_lazy('recipient_detail', kwargs={'pk':self.recipient.pk}),
                               reverse_lazy('vacation_create', kwargs={'recipient_id':self.recipient.pk}),
                               reverse_lazy('vacation_cancel', kwargs={'pk':self.vacation.pk})
                               ]
        self.login_url = reverse('auth_login')

    def test_not_logged_in(self):
        for url in self.login_required_urls:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 302)
            self.assertTrue(self.login_url in res['Location'])
            
    def test_logged_in(self):
        self.client.login(**self.userdata)
        for url in self.login_required_urls:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200)
            
    def test_wrong_owner(self):
        other_userdata = {'username':'not_xenuuu',
                          'password':'other_pass'}
        
        User.objects.create_user(**other_userdata)
        self.client.login(**other_userdata)
        
        for url in self.ownership_required_urls:
            res = self.client.get(url)
            if res.status_code != 404:
                print "Bug warning:  URL %s should return a 404 when interacting with somebody else's object.  But it returned a %s" % (url, res.status_code)
                
            #@todo:  These should all 404, but most do not.
            #Change this to an assertion instead of a warning after than code is implemented.
        
        
