from .generic_service_processor import GenericServiceProcessor
from .models import TumblrService
from pytumblr import TumblrRestClient

from django.conf import settings


class TumblrServiceProcessor(GenericServiceProcessor):
    def __init__(self, service=None):
        self.client = TumblrRestClient(consumer_key=settings.TUMBLR_API_KEY)
        self.tumblr_info = self.client.blog_info(service.tumblr_base_hostname)['blog']
        self.tumblr_post_list = []


    def connect(self, service=None):
        """
        Set our fields in the DB and save
        """

        #* Get avatar
        service.avatar = self.client.avatar(service.tumblr_base_hostname)['avatar_url']

        #* Get pretty name
        service.short_name = self.tumblr_info['name']
        service.pretty_name = self.tumblr_info['title']

        #* Get most recent post's timestamp
        service.last_post_ts = self.tumblr_info['updated']

        service.save()


    def grab(self, service=None):
        """
        Fill self.tumblr_post_list with posts
        """

        # First check if updated, if not, don't start pulling posts
        if(self.tumblr_info['updated'] <= service.last_poll_time):
            return

        # Get posts from blog and stop when we see one <= service.last_poll_time
        done_queueing = False

        while not done_queueing:
            twenty_posts = self.client.posts(service.tumblr_base_hostname,
                                             limit=20,
                                             offset=len(self.tumblr_post_list))['posts']

            for post in twenty_posts:
                if post['timestamp'] <= service.last_post_ts:
                    done_queueing = True
                    break
                else:
                    self.tumblr_post_list.append(post)


    def mangle(self):
        """
        Process the contents of self.tumblr_post_list and return as list
        """
        return self.tumblr_post_list
