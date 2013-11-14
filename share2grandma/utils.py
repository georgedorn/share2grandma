import sanetime
from sanetime import time, delta

def get_current_time_utc():
    """
    A wrapper for datetime.utcnow() which can be mocked.
    """
    return sanetime.time(tz='UTC')


def sanetime_to_bucket(sanetime_dt):
    """
    Returns the bucket for any given sanetime.  Minutes are rounded;

    minute [0, 30) -> bucket += 0
    minute [30, 60) -> bucket += 1

    Return:
        int. 0-47, where each int represents the 0-based number of the 30-min span starting at midnight UTC.
    """
    if not isinstance(sanetime_dt, sanetime.time):
        arg_class_name = sanetime_dt.__class__.__name__
        raise ValueError("expected sanetime.time, got %s" % arg_class_name)

    sanetime_dt.set_tz('UTC')

    if sanetime_dt.minute >= 30 and sanetime_dt.minute < 60:
        bucket_correct = 1
    else:
        bucket_correct = 0

    bucket = (sanetime_dt.hour * 2) + bucket_correct
    return bucket


def get_current_bucket():
    """
    Returns the current bucket based on UTC time.

    Return:
        int. 0-47, where each int represents a ~30min span starting at midnight.
    """
    now = get_current_time_utc()
    return sanetime_to_bucket(now)


def get_bucket(desired_time, timezone):
    """
    @param time a string in HH:MM:SS
    @param timezone an Olson string (e.g. "America/Los_Angeles")
    @return int a bucket_t, 0-47, with the bucket on today's date with above time and timezone
    """
    now = time(tz=timezone)
    desired_date = now.strftime('%Y-%m-%d')
    desired_time_with_date = "%s %s" % (desired_date, desired_time)
    desired_dt = sanetime.time(desired_time_with_date, tz=timezone)

    return sanetime_to_bucket(desired_dt)


def get_today_local_noon_dt(my_tz_name):
    now_dt = time(tz=my_tz_name)
    local_noon_dt = time(now_dt.year, now_dt.month, now_dt.day, 12, 0, 0, 0, tz=my_tz_name)
    return local_noon_dt

