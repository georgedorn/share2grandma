class GenericSubscriptionProcessor(object):
    """
    This is the interface for subscriptions.  They must have the
    methods below.
    """

    def __init__(self, subscription=None):
        """
        Constructor.

        Args:
            subscription: something that quacks like a GenericSubscription
        """
        self.subscription = subscription
        self.recipient = self.subscription.recipient
        self.content_items = []     # used for holding untransformed content items.


    @property
    def num_items_stored(self):
        """
        Returns:
            int number of content items currently stored.
        """
        return len(self.content_items)


    def setup_subscription(self):
        """
        Run when the user first sets up this subscription.

        Returns:
            dict of crap expected by convention by caller, or None.

        Raises:
            BorkedServiceException when the service is borked.
            BrokenServiceException when the service appears to need user intervention to return to a working state.
        """
        return None


    def pull_content(self):
        """
        Pulls data from the subscription and stores it in this object

        Returns:
            int Number of items stored, total.

        Raises:
            BorkedServiceException when the service is borked.
            BrokenServiceException when the service appears to need user intervention to return to a working state.
        """
        return 0


    def transform_content_longform(self):
        """
        Transforms pulled data to a long, full-email format we like, so we can send it.

        Returns:
            A list of strings, one for each object that should be dispatched, or None.
        """
        return None


    def transform_content_shortform(self, max=3):
        """
        Transforms pulled data to a short format we can add to DailyWakeups.

        Args:
            max: int, the max number of items that should be returned.  Defaults
                to 3.  The caller may lower this if DailyWakeup is getting too
                full.  Subclasses are responsible for returning the most important
                items if there is any sense of importance.  Will never be lower than
                1.

        Returns:
            A list of strings, or None.  Default is to return None (i.e., you must
            override this in subclasses or they won't contribute to DailyWakeup -
            and that's pretty common - this will be rarely overridden.)
        """
        return None