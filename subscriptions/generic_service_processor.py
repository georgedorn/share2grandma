class GenericSubscriptionProcessor(object):
    """
    This is the interface for services.  They must all have the
    methods below.
    """

    def get_blog_info(self):
        """
        Run when the user first sets up this service.
        """
        raise NotImplementedError


    def grab(self):
        """
        Pulls data from the service and stores it in this object
        """
        raise NotImplementedError


    def mangle(self):
        """
        Transforms pulled data to a format we like, so we can send it.
        returns string?
        """
        raise NotImplementedError

