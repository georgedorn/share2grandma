from django.test import TestCase
from share2grandma.utils import get_current_bucket, get_current_time_utc
from mock import patch
from datetime import datetime

def make_now_function(year=2013, month=11, day=12, hour=0, minute=0, second=0):
    """
    Generates a mock function for datetime.utcnow(), which when called
    returns the specified datetime object instead of utcnow().
    """
    return lambda: datetime(year=year, month=month, day=day,
                            hour=hour, minute=minute, second=second)

utc_fn_name = 'share2grandma.utils.get_current_time_utc'

class UtilsTests(TestCase):
    
    def test_get_current_bucket(self):
        with patch(utc_fn_name, make_now_function(hour=13, minute=48)):
            bucket = get_current_bucket()
            self.assertEqual(bucket, 27)
        
        with patch(utc_fn_name, make_now_function(hour=23, minute=59)):
            self.assertEqual(get_current_bucket(), 47)

        with patch(utc_fn_name, make_now_function(hour=0, minute=0)):
            self.assertEqual(get_current_bucket(), 0)
            
    def test_get_current_time_utc(self):
        """
        Mostly a test for coverage purposes; get_current_time_utc() is
        a patchable wrapper for datetime.utcnow().
        """
        now = get_current_time_utc()
        real_now = datetime.utcnow()
        
        diff = real_now - now
        self.assertLessEqual(diff.total_seconds(), 2)
        


