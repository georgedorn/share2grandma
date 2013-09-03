from datetime import datetime


def get_current_time_utc():
    """
    A wrapper for datetime.utcnow() which can be mocked.
    """
    return datetime.utcnow()

def get_current_bucket():
    """
    Returns the current bucket based on UTC time.

    Return:
        int. 0-47, where each int represents a ~30min span starting at midnight.
    """
    now = get_current_time_utc()
    if now.minute < 30:
        odd_bucket = 0
    else:
        odd_bucket = 1

    return (now.hour * 2) + odd_bucket
