from .models import TumblrSubscription
from .tumblr_service_processor import TumblrSubscriptionProcessor
from django.contrib.auth.models import User

from django.test import TestCase


class TumblrServiceProcessorTest(TestCase):
    """
    http://demo.tumblr.com/ is the 'fixture' in this case
    """

    def setUp(self):
        self.user = User.objects.create_user('derplord')
        self.service = TumblrSubscription(user=self.user,
                                     short_name='demo')
        self.tumblr = TumblrSubscriptionProcessor(self.service)


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


class TumblrServiceTest(TestCase):
    """
    http://demo.tumblr.com/ is the 'fixture' in this case
    """

    def setUp(self):
        self.user = User.objects.create_user('derplord')


    def test_update_from_tumblr(self):
        service = TumblrSubscription(short_name='demo')

        service.update_from_tumblr()

        self.assertTrue('default_avatar' in service.avatar)
        self.assertEqual('Demo', service.pretty_name)
        self.assertEqual(1269024321, service.last_post_ts)
