from .generic_subscription_processor import GenericSubscriptionProcessor


class DailyWakeupSubscriptionProcessor(GenericSubscriptionProcessor):
    def __init__(self, subscription=None):
        self.subscription = subscription

        # get all subscriptions for the user
        self.recipient = self.subscription.recipient
        self.recipient_subs = self.recipient.subscriptions.filter(enabled=True)


    def setup_subscription(self):
        """
        Get info about the blog from Tumblr
        """
        info = {}
        return info


    def pull_content(self):
        """
        Fill self.tumblr_post_list with posts
        """
        raise NotImplementedError


    def transform_content_longform(self):
        """
        Process the contents of self.tumblr_post_list and return as list
        """
        raise NotImplementedError

