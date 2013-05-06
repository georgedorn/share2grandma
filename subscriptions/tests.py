from .models import TumblrSubscription
from .tumblr_subscription_processor import TumblrSubscriptionProcessor
from django.contrib.auth.models import User

from django.test import TestCase


class TumblrSubscriptionProcessorTest(TestCase):
    """
    http://demo.tumblr.com/ is the 'fixture' in this case
    """

    def setUp(self):
        self.user = User.objects.create_user('derplord')
        self.subscription = TumblrSubscription(user=self.user,
                                     short_name='demo')
        self.tumblr = TumblrSubscriptionProcessor(self.subscription)


    def test_get_blog_info(self):
        info = self.tumblr.get_blog_info()

        self.assertTrue('default_avatar' in info['avatar'])
        self.assertEqual('Demo', info['pretty_name'])
        self.assertEqual(1269024321, info['last_post_ts'])


    def test_get_blog_info_baduser(self):
        pass


    def test_grab(self):
        pass


    def test_grab_no_new_posts(self):
        pass


    def test_mangle(self):
        pass


class TumblrSubscriptionTest(TestCase):
    """
    http://demo.tumblr.com/ is the 'fixture' in this case
    """

    def setUp(self):
        self.user = User.objects.create_user('derplord')


    def test_update_from_tumblr(self):
        subscription = TumblrSubscription(short_name='demo')

        subscription.update_from_tumblr()

        self.assertTrue('default_avatar' in subscription.avatar)
        self.assertEqual('Demo', subscription.pretty_name)
        self.assertEqual(1269024321, subscription.last_post_ts)