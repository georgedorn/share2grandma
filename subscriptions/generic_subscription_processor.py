class GenericSubscriptionProcessor(object):
    """
    This is the interface for subscriptions.  They must all have the
    methods below.
    """

    def setup_subscription(self):
        """
        Run when the user first sets up this subscription.

        Return: dict of crap expected by convention by caller, or None.
        """
        return None


    def pull_content(self):
        """
        Pulls data from the subscription and stores it in this object

        Return: int Number of items stored, total
        """
        return 0


    def transform_content_longform(self):
        """
        Transforms pulled data to a long, full-email format we like, so we can send it.

        Returns a list of strings, one for each object that should be dispatched, or None.
        """
        return None


    def transform_content_shortform(self):
        """
        Transforms pulled data to a short format we can add to DailyWakeups.

        Returns a list of strings, or None.  Default is to return None (i.e., you must
        override this in subclasses or they won't contribute to DailyWakeup -
        and that's pretty common - this will be rarely overridden.)
        """
        return None