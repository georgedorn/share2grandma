from .generic_subscription_processor import GenericSubscriptionProcessor


class DailyWakeupSubscriptionProcessor(GenericSubscriptionProcessor):
    """
    @todo WARNING XXX this processor needs to be run LAST, as all the others
    should've pulled content so they can return their shortform content if
    they have any.

    This is sort of pointing to a refactor where all Subscriptions pull,
    then the dailywakeup is just *generated* (it's not really a Subscription?)
    and then all the longform calls are made to the now-filled Subscription
    objects, and then each of those objects is dumped into the queue
    for dispatch.
    """
    def __init__(self, subscription=None):
        super(DailyWakeupSubscriptionProcessor, self).__init__(subscription)
        self.recipient_subs = self.recipient.subscriptions.filter(enabled=True)


    def pull_content(self):
        """
        Generate message here based on time, time zone, etc.
        """
        # @todo wakeup / postcode used to get weather


        # iterate over all recipient_subs and get their shortform content
        raise NotImplementedError


    def transform_content_longform(self):
        """
        Return the entire DailyWakeup email here.
        """
        email = "Hi Grandma, it's Tuesday, September 14th!"

        # @todo wakeup / add the weather bit

        # @todo wakeup / add all short-form content gotten at pull_content()

        # @todo wakeup / nice conclusion

        raise NotImplementedError
