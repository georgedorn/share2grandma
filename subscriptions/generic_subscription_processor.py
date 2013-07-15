class GenericSubscriptionProcessor(object):
    """
    This is the interface for subscriptions.  They must all have the
    methods below.
    """

    def get_blog_info(self):
        """
        Run when the user first sets up this subscription.
        """
        raise NotImplementedError


    def grab(self):
        """
        Pulls data from the subscription and stores it in this object
        """
        raise NotImplementedError


    def mangle(self):
        """
        Transforms pulled data to a format we like, so we can send it.
        returns string?
        """
        raise NotImplementedError


    def get_dailywakeup_string(self):
        """
        If implemented, returns a short bit of content to add to
        Daily Wakeup emails.
        """
        raise NotImplementedError
