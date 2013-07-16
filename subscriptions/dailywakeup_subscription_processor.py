from .generic_subscription_processor import GenericSubscriptionProcessor


class DailyWakeupSubscriptionProcessor(GenericSubscriptionProcessor):
    def __init__(self, subscription=None):
        self.subscription = subscription

        # get all subscriptions for the user
        self.recipient = self.subscription.recipient
        self.recipient_subs = self.recipient.subscriptions.filter(enabled=True)


    def pull_content(self):
        """
        Generate message here based on time, time zone, etc.
        """
        raise NotImplementedError


    def transform_content_shortform(self):
        """
        Return for DailyWakeup
        """
        raise NotImplementedError
