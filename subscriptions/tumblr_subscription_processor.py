from .generic_subscription_processor import GenericSubscriptionProcessor
from pytumblr import TumblrRestClient

from django.conf import settings


class TumblrSubscriptionProcessor(GenericSubscriptionProcessor):
    def __init__(self, subscription=None):
        self.subscription = subscription
        self.client = TumblrRestClient(consumer_key=settings.TUMBLR_API_KEY)
        blog_info_raw = self.client.blog_info(subscription.short_name)

        if 'meta' in blog_info_raw.keys():
            e_msg = "Status %s - %s" % (blog_info_raw['meta']['status'], blog_info_raw['meta']['msg'])
            if int(blog_info_raw['meta']['status']) == 404:
                raise KeyError, e_msg
            else:
                raise ValueError, e_msg

        self.tumblr_info = blog_info_raw['blog']
        self.tumblr_post_list = []


    def get_blog_info(self):
        """
        Get info about the blog from Tumblr
        """
        info = {}

        # Get avatar
        info['avatar'] = self.client.avatar(self.subscription.short_name)['avatar_url']

        # Get blog pretty_name
        info['pretty_name'] = self.tumblr_info['title']

        # Get most recent post's timestamp
        info['last_post_ts'] = self.tumblr_info['updated']

        return info


    def grab(self):
        """
        Fill self.tumblr_post_list with posts
        """

        # First check if updated, if not, don't start pulling posts
        if(self.tumblr_info['updated'] <= self.subscription.last_poll_time):
            return

        # Get posts from blog and stop when we see one <= self.subscription.last_poll_time
        done_queueing = False

        while not done_queueing:
            twenty_posts = self.client.posts(self.subscription.short_name,
                                             limit=20,
                                             offset=len(self.tumblr_post_list))['posts']

            for post in twenty_posts:
                if post['timestamp'] <= self.subscription.last_post_ts:
                    done_queueing = True
                    break
                else:
                    self.tumblr_post_list.append(post)


    def mangle(self):
        """
        Process the contents of self.tumblr_post_list and return as list
        """
        return self.tumblr_post_list
