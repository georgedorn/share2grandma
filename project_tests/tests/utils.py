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
    def test_get_current_time_utc(self):
        """
        Mostly a test for coverage purposes; get_current_time_utc() is
        a patchable wrapper for datetime.utcnow().
        """
        now = get_current_time_utc()
        real_now = datetime.utcnow()
        
        diff = real_now - now
        self.assertLessEqual(diff.total_seconds(), 2)
        

class GetBucketTests(TestCase):

    def test_get_bucket_ultra_basic_tests(self):
        with patch(utc_fn_name, make_now_function(hour=13, minute=48)):
            bucket = get_current_bucket()
            self.assertEqual(bucket, 27)

        with patch(utc_fn_name, make_now_function(hour=23, minute=59)):
            self.assertEqual(get_current_bucket(), 47)

        with patch(utc_fn_name, make_now_function(hour=0, minute=0)):
            self.assertEqual(get_current_bucket(), 0)


    def test_get_bucket_summerwinter_non_dst_zones(self):
        ## Africa/Dar_es_Salaam
        #self.assertEqual(result, expect,
        #                 "Expected %d for %s (interpreted as %s), got %d" % (expect, recip.timezone, tz_interp, result))
        #
        ## Argentina/Buenos_Aires
        #self.assertEqual(result, expect,
        #                 "Expected %d for %s (interpreted as %s), got %d" % (expect, recip.timezone, tz_interp, result))
        #
        ## America/Phoenix
        #self.assertEqual(result, expect,
        #                 "Expected %d for %s (interpreted as %s), got %d" % (expect, recip.timezone, tz_interp, result))
        #
        ## Asia/Saigon
        #self.assertEqual(result, expect,
        #                 "Expected %d for %s (interpreted as %s), got %d" % (expect, recip.timezone, tz_interp, result))
        self.skipTest('writeme')


    def test_get_bucket_summerwinter_non_dst_weird_zones(self):
        #"""
        #no DST but non-even minutes
        #"""
        #
        ## Asia/Katmandu		+05:45	+05:45
        #self.assertEqual(result, expect,
        #                 "Expected %d for %s (interpreted as %s), got %d" % (expect, recip.timezone, tz_interp, result))
        #
        ## Asia/Calcutta		+05:30	+05:30
        #self.assertEqual(result, expect,
        #                 "Expected %d for %s (interpreted as %s), got %d" % (expect, recip.timezone, tz_interp, result))
        #
        ## Pacific/Marquesas
        #self.assertEqual(result, expect,
        #                 "Expected %d for %s (interpreted as %s), got %d" % (expect, recip.timezone, tz_interp, result))
        self.skipTest('writeme')


    def test_get_bucket_summerwinter_dst_zones(self):
        # America/Resolute
        #June
        #specified_local_noon_dt = datetime.combine(date(2013, 6, 15), time(12, 0, 0, 0, tzinfo=tz))
        #recip.__get_local_noon_dt = Mock(return_value=specified_local_noon_dt)
        #tz_interp = datetime.now(tz=recip.timezone).tzname()
        #expect = 4
        #result = recip.localnoon_hour
        #self.assertEqual(result, expect,
        #                 "Expected %d for %s in %s (interpreted as %s), got %d" % (expect, specified_local_noon_dt, recip.timezone, tz_interp, result))
        #
        ## America/Chicago
        ## Europe/Copenhagen
        ## Australia/Hobart
        self.skipTest('writeme')


    def test_get_bucket_summerwinter_dst_weird_zones(self):
        # DST with non-even minutes
        # America/St_Johns
        # Pacific/Chatham
        self.skipTest('writeme')
