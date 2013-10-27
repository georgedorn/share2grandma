import re
from datetime import date
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core import mail
from django.test import TestCase
from django.utils import timezone as dutz

from .models import TumblrSubscription, Recipient, Vacation
from .forms import TumblrSubscriptionForm, RecipientForm, VacationForm
import pytz
import locale

from subscriptions.forms import VacationForm
from django.template.context import Context
from django.template.base import Template
from subscriptions.models import GenericSubscription

class GenericSubscriptionTest(TestCase):
    """
    Tests of the generic subscription model.
    Probably silly, other than proving the API.
    """
    
    def test_pull_content(self):
        foo = GenericSubscription()
        self.assertRaises(NotImplementedError, foo.pull_content)
        
    def test_pull_metadata(self):
        foo = GenericSubscription()
        self.assertRaises(NotImplementedError, foo.pull_metadata)
    
    def test_format_content(self):
        foo = GenericSubscription()
        self.assertRaises(NotImplementedError, foo.format_content, "This is content")


class TumblrSubscriptionProcessorTest(TestCase):
    """
    http://demo.tumblr.com/ is the 'fixture' in this case
    """

    def setUp(self):
        self.user = User.objects.create_user('derplord')
        self.recipient = Recipient.objects.create(sender=self.user,
                                                  name='Grrrranny',
                                                  email='mams@aol.com')
        self.subscription = TumblrSubscription(recipient=self.recipient,
                                               short_name='demo')


    def test_get_blog_info(self):
        self.subscription.pull_metadata()
        self.assertTrue('default_avatar' in self.subscription.avatar)
        self.assertEqual('Demo', self.subscription.pretty_name)
        self.assertEqual(1269024321, self.subscription.last_post_ts)
        

    def test_instantiate_badblog(self):
        caught = False
        try:
            my_subscription = TumblrSubscription(recipient=self.recipient,
                                             short_name='zmxmdmcnnjjncn')
            my_subscription.pull_metadata()
        except KeyError, e:
            caught = True

        self.assertTrue(caught, "Didn't catch expected exception with bad blog name.")


    def test_num_items_stored(self):
        # @todo
        raise self.skipTest('write me')


    def test_pull_content(self):
        # @todo
        raise self.skipTest('write me')


    def test_pull_content_no_new_posts(self):
        # @todo
        raise self.skipTest('write me')


    def test_transform_content_longform(self):
        # @todo
        raise self.skipTest('write me')


    def test_transform_content_shortform(self):
        # @todo
        raise self.skipTest('write me')


    def test_transform_content_shortform_low_max(self):
        # @todo
        raise self.skipTest('write me')


    
class SubscriptionTestCase(TestCase):

    def render_variable_in_template(self, variable):
        t = Template('{{ variable }}')
        c = Context({"variable": variable})
        return t.render(c)

    
    def setUp(self):
        self.userdata = {'username':'xenuuu',
                         'password':'test_pass'}
        self.user = User.objects.create_user(**self.userdata)
        self.user = User.objects.get_by_natural_key('xenuuu')

        self.recipient = Recipient.objects.create(sender=self.user,
                                                  name='Nonna',
                                                  email='elsa@yahoo.com',
                                                  postcode='02540')


class ProfileTestCase(SubscriptionTestCase):
    """
    Test the extended user profile and whatnot.
    """
    def test_model_save_email_gen(self):
        """
        in setUp(), this should have fired.
        """
        pattern = r's2g_[a-zA-Z0-9_\-]{8}'
        self.assertTrue(re.match(pattern, self.user.s2g_profile.s2g_email),
                        'expected s2g email s2g + 8 random chars but got: %s' % self.user.s2g_profile.s2g_email)

    def test_email_visible(self):
        # @todo
        self.skipTest('write me')


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
        subscription.recipient = self.recipient

        subscription.pull_metadata()

        self.assertTrue('default_avatar' in subscription.avatar)
        self.assertEqual('Demo', subscription.pretty_name)
        self.assertEqual(1269024321, subscription.last_post_ts)

    def test_update_from_nonexistent_tumblr(self):
        """
        not via UI, tumblr which doesn't exist
        """
        self.skipTest('writeme')

    def test_update_from_temporarily_borked_tumblr(self):
        """
        Simulate a server error that's likely temporary
        """
        self.skipTest('writeme')

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
            {'recipient':self.recipient.pk,
             'short_name':'demo',
             'enabled':True},
            follow=True)

        obj = TumblrSubscription.objects.get(short_name='demo', recipient=self.recipient)
        self.assertTrue(isinstance(obj, TumblrSubscription))
        self.assertEqual(obj.num_borked_calls, 0)
        self.assertEqual(obj.first_borked_call_time, None)
        self.assertFalse(obj.appears_broken)

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

    def test_subscription_detail_view(self):
        # does this exist somewhere else?
        self.skipTest('writeme')

    def test_subscription_detail_view_somebody_elses_subscription(self):
        self.skipTest('writeme')

    def test_delete_somebody_elses_tumblr_subscription(self):
        self.skipTest('writeme')

    def test_create_somebody_elses_tumblr_subscription(self):
        self.skipTest('writeme')

    def test_create_tumblr_subscription_nonexistent_recipient(self):
        self.skipTest('writeme')

    def test_create_tumblr_subscription_somebody_elses_recipient(self):
        self.skipTest('writeme')

    def test_login_required(self):
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

    def test_pull_content(self):
        self.skipTest('writeme')

    def test_pull_content_temporarily_borked_tumblr(self):
        self.skipTest('writeme')

    def test_pull_content_temporarily_borked_tumblr_5_times(self):
        self.skipTest('writeme')

    def test_pull_content_broken_tumblr(self):
        self.skipTest('writeme')



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
            {'sender':self.user.pk, #@todo: Sender is not posted, should be in request
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

        granny_data.pop('sender')     # not looking for pk in output
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
        self.skipTest('writeme')


    def test_delete_somebody_elses_recipient(self):
        self.skipTest('writeme')


    def test_create_somebody_elses_recipient(self):
        self.skipTest('writeme')


    def test_create_recipient_nonexistent_user(self):
        self.skipTest('writeme')


    def test_detail_view(self):
        """
        Test that the Recipient detail view displays the right stuff

        @todo:  This is extremely fragile and should be rewritten to test fields explicitly
        """
        self.client.login(**self.userdata)

        res = self.client.get(reverse('recipient_detail', kwargs={'pk':self.recipient.pk}),
            follow=True)

        expected_fields = ('sender_name', 'sender_phone', 'name', 'add_date',
                           'email', 'postcode')
        
        for field in expected_fields:
            v = getattr(self.recipient, field)
            rendered_variable = self.render_variable_in_template(v)
            self.assertTrue(rendered_variable in res.rendered_content,
                            "Expected value '%s' for field '%s' in rendered content %s" % (v, field, res.content))

    def test_detail_view_somebody_elses_recipient(self):
        self.skipTest('writeme')


    def test_dashboard_recipient_display(self):
        """
        Test that the Recipient shows up on the dashboard
        
        @todo:  This is extremely fragile and should be rewritten to test fields explicitly
        """
        self.client.login(**self.userdata)

        res = self.client.get(reverse('dashboard_main'), follow=True)
        
        
        expected_fields = ('sender_name', 'sender_phone', 'name', 'add_date',
                           'email', 'postcode')
        
        for field in expected_fields:
            v = getattr(self.recipient, field)
            rendered = self.render_variable_in_template(v)

            self.assertTrue(rendered in res.rendered_content,
                            "Expected value '%s' for field '%s' in rendered content" % (v, field))

    def test_calculate_localnoon_bucket_string_timezone(self):
        self.skipTest('writeme')

    def test_calculate_localnoon_bucket_datetimezone(self):
        self.skipTest('writeme')

    def test_calculate_localnoon_bucket_noargs(self):
        self.skipTest('writeme')

    def test_calculate_localnoon_halfhour_timezone(self):
        # use America/St_Johns, bucket should be incremented by 1.
        self.skipTest('writeme')

    def test_calculate_delivery_buckets(self):
        self.skipTest('writeme')

    def test_calculate_delivery_buckets_no_args(self):
        self.skipTest('writeme')
        
    def test_set_dailywakeup_bucket(self):
        self.recipient.dailywakeup_hour = 6
        self.recipient.dailywakeup_bucket = None #redundant, but in case we change the init logic
        self.recipient.set_dailywakeup_bucket(delete=False)
        self.assertTrue(self.recipient.dailywakeup_bucket is not None) #@todo: once bucket logic is settled, test the actual value
        
    def test_set_dailywakeup_bucket_delete(self):
        self.recipient.dailywakeup_hour = 6
        self.recipient.dailywakeup_bucket = 12 #arbitrary
        self.recipient.save()
        self.recipient.set_dailywakeup_bucket(delete=True)
        self.assertTrue(self.recipient.dailywakeup_bucket is None)

    def test_get_recipients_due_for_processing(self):
        """
        Just a simple test of the query, not the bucket logic itself.
        """
        Recipient.objects.all().delete() #@todo: move this into another test case that doesn't create Recipient objects by default and remove this line
        self.recipients = []
        for i in range(10):
            recip = Recipient(sender=self.user,
                              name="Recip%s" % i,
                              email='recip%s@yahoo.com' % i,
                              postcode='11111',
                              )
            #these buckets make no sense, but we're testing the query and need some overlay
            recip.dailywakeup_bucket = i / 2 
            recip.morning_bucket = 3 + i / 2
            recip.evening_bucket = 6 + i / 3 
            recip.wee_hours_bucket = 9 + i / 3 
            recip.save()

        #the results of the above mess, 
        #    D M E W
        #    0 3 6 9
        #    0 3 6 9
        #    1 4 6 9
        #    1 4 7 10
        #    2 5 7 10
        #    2 5 7 10
        #    3 6 8 11
        #    3 6 8 11
        #    4 7 8 11
        #    4 7 9 12

        #and this is how many recipients have at least one bucket set to each value (e.g. 2 recipients have a 0 bucket            
        expected = {0:2, 1:2, 2:2, 3:4, 4:4, 5:2, 6:5, 
                    7:5, 8:3, 9:4, 10:3, 11:3, 12:1
                   }

        for bucket, count in expected.items():
            due_count = Recipient.get_recipients_due_for_processing(bucket).count()
            try:
                self.assertEqual(due_count, count, 
                         "Expected %s recipients in bucket %s, got %s" % (count, bucket, due_count))
            except AssertionError, e:
                print e
                for recip in Recipient.objects.all():
                    print recip.dailywakeup_bucket, recip.morning_bucket, recip.evening_bucket, recip.wee_hours_bucket
                raise

    def test_dispatch(self):
        self.recipient.dispatch("This is the content")
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.body, "This is the content")
        self.assertTrue(msg.from_email.startswith(self.recipient.sender.s2g_profile.s2g_email))
        self.assertEqual(msg.to, [self.recipient.email])
        #@todo: subject line?
        

    def test_deliver_non_daily_wakeup(self):
        """
        Test that a tumblr subscription item is delivered.
        """
        subscription = TumblrSubscription.objects.create(recipient=self.recipient,
                                          short_name='demo',
                                          pretty_name='demo',
                                          )
        self.recipient.deliver(0)

        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]

        self.assertTrue("Lorem ipsum dolor sit amet" in msg.body)

        html = msg.alternatives[0][0]
        self.assertTrue("Lorem ipsum dolor sit amet" in html)

        
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
                                
    def test_get_vacationing_recipients(self):
        """
        Tests getting the set of recipients currently on vacation.
        """
        #start with a clean slate
        Recipient.objects.all().delete()
        now = dutz.now()
        last_week = now - timedelta(days=7)
        next_week = now + timedelta(days=7)
        
        for i in range(10):
            recipient = Recipient.objects.create(sender=self.user,
                                     name='Nonna_%s' % i,
                                     email='elsa_%s@yahoo.com' % i,
                                     postcode='02540')
                    
            if i < 4: #create vacations for the first four
                Vacation.objects.create(recipient=recipient,
                                        start_date=last_week,
                                        end_date=next_week)
        
        self.assertEqual(Recipient.get_vacationing_recipients().count(), 4)
        self.assertEqual(Recipient.objects.exclude(pk__in=Recipient.get_vacationing_recipients()).count(), 6)
                

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
        
        self.assertEqual(vacation.start_date.tzinfo, timezone)
        self.assertEqual(vacation.end_date.tzinfo, timezone)
        
    def test_bad_vacation_form(self):
        """
        Submitting a vacation form where the start date is after the end date is an error.
        """
        start = dutz.now().today()
        end = start - timedelta(days=1)
        data = {'start_date': start.strftime('%Y-%m-%d'),
                'end_date': end.strftime('%Y-%m-%d')}
        form = VacationForm(data)
        self.assertFalse(form.is_valid())
        
    def test_delete_future_vacation(self):
        """
        Cancelling a future vacation that has not yet started is fine,
        just delete it.
        """
        self.client.login(**self.userdata)
        start = dutz.now() + timedelta(days=1)
        end = start + timedelta(weeks=1)
        vacation = Vacation.objects.create(recipient=self.recipient,
                                           start_date=start,
                                           end_date=end
                                           )
        
        url = reverse('vacation_cancel', kwargs={'pk':vacation.pk})
        self.client.post(url)
        
        self.assertRaises(Vacation.DoesNotExist, Vacation.objects.get, pk=vacation.pk)
    
    def test_delete_started_vacation(self):
        """
        Cancelling a vacation that's already started actually sets 
        the end date to now, not actually deleting it.
        """
        self.client.login(**self.userdata)
        start = dutz.now() - timedelta(days=2) #started yesterday
        end = start + timedelta(days=7)
        vacation = Vacation.objects.create(recipient=self.recipient,
                                           start_date=start,
                                           end_date=end
                                           )
        
        url = reverse('vacation_cancel', kwargs={'pk':vacation.pk})
        self.client.post(url)
        vacation = Vacation.objects.get(pk=vacation.pk) #reload
        self.assertTrue(vacation.end_date <= dutz.now())

    def test_delete_somebody_elses_vacation(self):
        """
        Users shouldn't be able to delete vacations belonging to other users.
        """
        new_user = User.objects.create_user("new_user", password='new_pass')
        new_recipient = Recipient.objects.create(sender=new_user,
                                                  name='Nanna',
                                                  email='elsie@yahoo.com')

        #this vacation starts and ends in the future, so it can be deleted and not just trigger
        #the end_date change.
        vacation = Vacation.objects.create(recipient=new_recipient,
                                           start_date=dutz.now() + timedelta(days=1),
                                           end_date=dutz.now() + timedelta(weeks=4))
        url = reverse('vacation_cancel', kwargs={'pk':vacation.pk})
        
        self.client.login(**self.userdata) #login as self.user, NOT new_user
        
        #try to delete vacation belonging to new_user
        res = self.client.post(url)
        vacation = Vacation.objects.get(pk=vacation.pk) #force reload, should still exist

    def test_create_somebody_elses_vacation(self):
        new_user = User.objects.create_user("new_user", password='new_pass')
        new_recipient = Recipient.objects.create(sender=new_user,
                                                  name='Nanna',
                                                  email='elsie@yahoo.com')

        self.client.login(**self.userdata)
        url = reverse('vacation_create', kwargs={'recipient_id': new_recipient.pk})
        
        start = dutz.now().today()
        end = start - timedelta(days=1)
        data = {'start_date': start.strftime('%Y-%m-%d'),
                'end_date': end.strftime('%Y-%m-%d')}
        
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 404) #can't do that
        
        

