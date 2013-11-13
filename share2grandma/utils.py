from datetime import datetime
import sanetime
import pytz

def get_current_time_utc():
    """
    A wrapper for datetime.utcnow() which can be mocked.
    """
    return sanetime.time()


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


def get_bucket(desired_time, timezone):
    """
    @param time a string in HH:MM:SS
    @param timezone an Olson string (e.g. "America/Los_Angeles" or pytz.tzinfo instance
    @return int a bucket_t, 0-47, with the bucket on today's date with above time and timezone
    """
    tz = pytz.timezone(timezone)
    now = get_current_time_utc()
    now.set_tz(tz)
    desired_date = now.strftime('%Y-%m-%d')
    desired_time_with_date = "%s %s" % (desired_time, desired_date)

    desired_dt = sanetime.time(desired_time_with_date, tz=timezone)
    hour = desired_dt.utc_datetime.hour
    minute = desired_dt.utc_datetime.minute


    bucket = 2 * hour
    bucket += (minute/30) # adds 1 if minute greater or equal to 30
    return bucket



