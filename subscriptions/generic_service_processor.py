# This is the interface for services.  They must all have the
# methods below.


class GenericServiceProcessor(object):
    def grab():
        """Pulls data from the service and stores it in this object"""
        raise NotImplementedError


    def mangle():
        """
        Transforms pulled data to a format we like, so we can send it.
        returns string?
        """
        raise NotImplementedError

