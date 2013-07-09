from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone as dutz

from .models import TumblrSubscription, Recipient, Vacation
from .forms import TumblrSubscriptionForm, RecipientForm
from .tumblr_subscription_processor import TumblrSubscriptionProcessor
import pytz

def fixed_now():
    """
    Returns a constant datetime object, instead of now().
    """
    return datetime(2012, 12, 12)


class TumblrSubscriptionProcessorTest(TestCase):
    """
    http://demo.tumblr.com/ is the 'fixture' in this case
    """

    def setUp(self):
        self.user = User.objects.create_user('derplord')
        self.recipient = Recipient.objects.create(user=self.user,
                                                  name='Grrrranny',
                                                  email='mams@aol.com')
        self.subscription = TumblrSubscription(recipient=self.recipient,
                                               short_name='demo')
        self.tumblr = TumblrSubscriptionProcessor(self.subscription)


    def test_get_blog_info(self):
        info = self.tumblr.get_blog_info()

        self.assertTrue('default_avatar' in info['avatar'])
        self.assertEqual('Demo', info['pretty_name'])
        self.assertEqual(1269024321, info['last_post_ts'])


    def test_instantiate_badblog(self):
        my_subscription = TumblrSubscription(recipient=self.recipient,
                                             short_name='zmxmdmcnnjjncn')
        caught = False
        try:
            TumblrSubscriptionProcessor(my_subscription)
        except KeyError, e:
            caught = True

        self.assertTrue(caught, "Didn't catch expected exception with bad blog name.")


    def test_grab(self):
        # @todo
        pass


    def test_grab_no_new_posts(self):
        # @todo
        pass


    def test_mangle(self):
        # @todo
        pass
    
    
class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.userdata = {'username':'xenuuu',
                         'password':'test_pass'}
        self.user = User.objects.create_user(**self.userdata)
        self.user = User.objects.get_by_natural_key('xenuuu')

        self.recipient = Recipient.objects.create(user=self.user,
                                                  name='Nonna',
                                                  email='elsa@yahoo.com')



class TumblrSubscriptionTest(SubscriptionTestCase):
    """
    http://demo.tumblr.com/ is the 'fixture' in this case
    """
    def setUp(self):
        super(TumblrSubscriptionTest, self).setUp()
        self.login_url = reverse('auth_login')
        self.url_subscription_create_tumblr = reverse('subscription_create_tumblr')

    def test_update_from_tumblr(self):
        """
        not via UI
        """
        subscription = TumblrSubscription(short_name='demo')

        subscription.update_from_tumblr()

        self.assertTrue('default_avatar' in subscription.avatar)
        self.assertEqual('Demo', subscription.pretty_name)
        self.assertEqual(1269024321, subscription.last_post_ts)

    def test_create_tumblr_subscription_form_exists(self):
        """
        UI
        """
        self.client.login(**self.userdata)

        res = self.client.get(self.url_subscription_create_tumblr)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context[0].has_key('form'))
        self.assertTrue(isinstance(res.context[0].get('form'), TumblrSubscriptionForm))

    def test_create_tumblr_subscription_via_ui(self):
        self.client.login(**self.userdata)

        res = self.client.post(self.url_subscription_create_tumblr,
            {'user':self.user.pk,
             'recipient':self.recipient.pk,
             'short_name':'demo',
             'enabled':True},
            follow=True)

        obj = TumblrSubscription.objects.get(short_name='demo', recipient=self.recipient)
        self.assertTrue(isinstance(obj, TumblrSubscription))

        success = False
        for url, status in res.redirect_chain:
            if reverse('subscription_detail_tumblr', kwargs={'pk':obj.pk}) in url:
                if status >= 301 and status <= 302:
                    # this redirect chain is a bit weird and might change, so be flexible..
                    # we got redirected to the detail url for what we just created, so yay
                    success = True
        self.assertTrue(success)

        self.assertTrue('default_avatar_64.png' in res.rendered_content)
        self.assertTrue('Demo' in res.rendered_content)
        self.assertTrue(self.user.username in res.rendered_content)

    def test_delete_subscription(self):
        subscription = TumblrSubscription(short_name='demo', recipient=self.recipient)
        subscription.save()

        sub_all = TumblrSubscription.objects.all()
        result = len(sub_all)
        self.assertEqual(result, 1)

        new_sub = TumblrSubscription.objects.get(short_name='demo')
        new_sub.delete()

        del_sub = TumblrSubscription.objects.all()
        result = len(del_sub)
        self.assertEqual(result, 0)

    def test_delete_subscription_via_url(self):
        subscription = TumblrSubscription(short_name='demo', recipient=self.recipient)
        subscription.save()

        subscription = TumblrSubscription.objects.get(pk=subscription.pk)
        self.assertTrue(isinstance(subscription, TumblrSubscription))
        num_subscriptions = len(TumblrSubscription.objects.all())

        self.client.login(**self.userdata)

        res = self.client.get(reverse('subscription_delete_tumblr',
                                      kwargs={'pk':subscription.pk}))

        self.assertEqual(res.status_code, 200)
        self.assertTrue('Are you sure' in res.rendered_content)
        res = self.client.post(reverse('subscription_delete_tumblr',
                                      kwargs={'pk':subscription.pk}),
                               data={'submit':'Delete'},
                               follow=True)

        # at the end of the redirect chain...
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(res.redirect_chain) >= 1)

        # make sure we have one fewer TumblrSubscriptions than before
        self.assertEqual(len(TumblrSubscription.objects.all()), num_subscriptions - 1)

    def test_login_require(self):
        subscription = TumblrSubscription(short_name='demo', recipient=self.recipient)
        subscription.save()

        obj = TumblrSubscription.objects.get(short_name='demo', recipient=self.recipient)
        self.assertTrue(isinstance(obj, TumblrSubscription))

        pages = [reverse('subscription_create_tumblr'), reverse('subscription_delete_tumblr', kwargs={'pk':obj.pk}),
                 reverse('subscription_detail_tumblr', kwargs={'pk':obj.pk}), reverse('subscription_list')]

        for page in pages:
            res = self.client.get(page, follow=True)

            success = False
            for url, status in res.redirect_chain:
                if reverse('auth_login') in url:
                    if status >= 301 and status <= 302:
                        success = True
            self.assertTrue(success)


class RecipientTest(SubscriptionTestCase):
    """
    http://demo.tumblr.com/ is the 'fixture' in this case
    """

    def setUp(self):
        super(RecipientTest, self).setUp()
        self.login_url = reverse('auth_login')
        self.url_recipient_create = reverse('recipient_create')


    def test_create_recipient_form_exists(self):
        """
        Test that the form is there and non-500, etc
        """
        self.client.login(**self.userdata)

        res = self.client.get(self.url_recipient_create)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context[0].has_key('form'))
        self.assertTrue(isinstance(res.context[0].get('form'), RecipientForm))


    def test_create_recipient_via_ui(self):
        """
        Use the create form and test that it works right.
        """
        self.client.login(**self.userdata)

        granny_data = \
            {'user':self.user.pk,
             'sender_name':'bobby',
             'sender_phone':'111-222-3344',
             'name':'Granny Em',
             'email':'emgran@aol.com',
             'timezone':'America/Indiana/Knox'
             }

        res = self.client.post(self.url_recipient_create,
            granny_data,
            follow=True)

        self.assertTrue(Recipient.objects.count() == 2)  # includes fixture

        obj = Recipient.objects.get(name='Granny Em')
        self.assertTrue(isinstance(obj, Recipient))

        success = False
        for url, status in res.redirect_chain:
            if reverse('recipient_detail', kwargs={'pk':obj.pk}) in url:
                if status >= 301 and status <= 302:
                    # this redirect chain is a bit weird and might change, so be flexible..
                    # we got redirected to the detail url for what we just created, so yay
                    success = True
        self.assertTrue(success)

        granny_data.pop('user')     # not looking for pk in output
        self.assertTrue(self.user.username in res.rendered_content)

        for s in granny_data.values():
            self.assertTrue(s in res.rendered_content,
                            'Expected "%s" in rendered_content' % s)


    def test_delete(self):
        """
        Delete a Recipient object directly
        # @todo use this to test that recipient subscriptions and so on all go with?
        """
        self.assertTrue(self.user.recipients.count() == 1)
        self.recipient.delete()
        self.assertTrue(self.user.recipients.count() == 0)


    def test_delete_via_ui(self):
        """
        Delete a Recipient via the UI
        """
        # not yet implemented, different story
        pass


    def test_detail_view(self):
        """
        Test that the Recipient detail view displays the right stuff
        """
        self.client.login(**self.userdata)

        res = self.client.get(reverse('recipient_detail', kwargs={'pk':self.recipient.pk}),
            follow=True)

        for field in self.recipient._meta.fields:
            v = getattr(self.recipient, field.name)

            if field.name == 'add_date':
                v = v.strftime('%B %d, %Y')     # @todo: use whatever Django's using instead of hardcoding

            self.assertTrue(str(v) in res.rendered_content,
                            "Expected value '%s' for field '%s' in rendered content" % (v, field))


    def test_dashboard_recipient_display(self):
        """
        Test that the Recipient shows up on the dashboard
        """
        self.client.login(**self.userdata)

        res = self.client.get(reverse('dashboard_main'), follow=True)

        for field in self.recipient._meta.fields:
            v = getattr(self.recipient, field.name)

            if field.name == 'add_date':
                v = v.strftime('%B %d, %Y')     # @todo: use whatever Django's using instead of hardcoding
            if field.name == 'timezone':
                continue    # not currently displayed.

            self.assertTrue(str(v) in res.rendered_content,
                            "Expected value '%s' for field '%s' in rendered content" % (v, field))


class VacationTests(SubscriptionTestCase):
    
    def test_not_on_vacation(self):
        self.assertFalse(self.recipient.is_on_vacation())

    def test_is_on_vacation_obvious(self):
        now = dutz.now()
        last_week = now - timedelta(days=7)
        next_week = now + timedelta(days=7)
        Vacation.objects.create(recipient=self.recipient,
                                start_date=last_week,
                                end_date=next_week)
        
        self.assertTrue(self.recipient.is_on_vacation())

    def test_is_not_on_vacation_timezone(self):
        """
        A test of an edge case where a recipient's vacation is in a different time zone than the server.
        """
        timezone = pytz.timezone('Europe/Amsterdam')
        self.recipient.timezone = timezone
        self.recipient.save()
        now = datetime.now()
        
        #the trick here is that pytz.timezone.localize takes a naive datetime
        #and appends a timezone without altering the datetime.
        #e.g. if it is 8pm now in America/Los_Angeles,
        #this results in a start of 6pm in Europe/Amsterdam
        start = timezone.localize(now - timedelta(hours=2))
        #and this would result in end of 10pm in Europe/Amsterdam
        end = timezone.localize(now + timedelta(hours=2))
        
        Vacation.objects.create(recipient=self.recipient,
                                start_date=start,
                                end_date=end)
        #Amsterdam is 8-9 hours ahead depending on DST, so this 4-hour vacation
        #was actually over about 4 hours ago
        self.assertFalse(self.recipient.is_on_vacation())
        
    def test_is_on_vacation_timezone(self):
        """
        Like previous test, create a vacation in another timezone, but
        make it overlap the current time in the server's timezone.
        """
        timezone = pytz.timezone('Europe/Amsterdam') # 8-9 hours ahead
        self.recipient.timezone = timezone
        self.recipient.save()
        
        now = datetime.now()
        
        start = timezone.localize(now + timedelta(hours=6)) #less than 8-9 hours from now
        end = timezone.localize(now + timedelta(hours=12))
        
        Vacation.objects.create(recipient=self.recipient,
                                start_date=start,
                                end_date=end
                                )
        self.assertTrue(self.recipient.is_on_vacation())
                                

    def test_stupid_vacation(self):
        """
        Ensure that creating a vacation without timezone info results
        in using the recipient's timezone.
        """
        timezone = pytz.timezone('America/New_York')
        self.recipient.timezone = timezone
        self.recipient.save()
        
        start = datetime(year=2012, month=12, day=12, hour=12)
        end = datetime(year=2012, month=12, day=14, hour=12)
        
        vacation = Vacation.objects.create(recipient=self.recipient,
                                           start_date=start,
                                           end_date=end)
        
        self.assertEqual(vacation.start_date.tzinfo,
                         timezone)
        self.assertEqual(vacation.end_date.tzinfo,
                         timezone)
