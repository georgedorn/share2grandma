"""
Exceptions unique to the subscriptions app.
"""

class BrokenServiceException(Exception):
    """
    Thrown when somebody gets an indication that the Service in question is actually *broken* (eg permanent OAuth fail)
    and needs attention.
    """
    pass


class BorkedServiceException(Exception):
    """
    Thrown when a service is borked for any reason.  This generally implies temporariness,
    could be a timeout or 500 etc.
    """
    pass
