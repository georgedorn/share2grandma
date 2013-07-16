class GenericSubscriptionProcessor(object):
    """
    This is the interface for subscriptions.  They must all have the
    methods below.
    """

    def setup_subscription(self):
        """
        Run when the user first sets up this subscription.
        """
        raise NotImplementedError


    def pull_content(self):
        """
        Pulls data from the subscription and stores it in this object
        """
        raise NotImplementedError


    def transform_content_longform(self):
        """
        Transforms pulled data to a format we like, so we can send it.
        returns string?
        """
        raise NotImplementedError


    def transform_content_shortform(self):
        """
        If implemented, returns a short bit of content to add to
        Daily Wakeup emails.
        """
        raise NotImplementedError
