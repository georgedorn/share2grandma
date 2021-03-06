from django.test import TestCase
from share2grandma.utils import get_current_bucket, get_current_time_utc, get_today_bucket_for_time
from mock import patch
from sanetime import time


def make_now_function(year=2013, month=11, day=12, hour=0, minute=0, second=0, tz='UTC'):
    """
    Generates a mocka function for, which when called
    returns the specified datetime object instead of utcnow().
    
    Used for mocking share2grandma.utils.get_current_time_utc.
    """

    #convert kwargs to positional args, as sanetime sadly doesn't take kwargs.
    args = [year, month, day, hour, minute, second]

    def my_func():
        dt = time(*args, tz=tz)
        return dt

    return my_func


#Function name to patch() with make_now_function instead.
UTC_FN_NAME = 'share2grandma.utils.get_current_time_utc'

class UtilsTests(TestCase):
    def test_get_current_time_utc(self):
        """
        Mostly a test for coverage purposes, but also ensures get_current_time_utc() isn't doing
        something crazy under normal circumstances.
        """
        now = get_current_time_utc()
        real_now = time(tz='UTC')
        
        delt = real_now - now
        self.assertLessEqual(delt.whole_seconds, 2)
        

class GetBucketTests(TestCase):

    def test_get_bucket_ultra_basic_tests(self):
        """
        Simple tests of get_current_bucket().
        """
        with patch(UTC_FN_NAME, make_now_function(hour=13, minute=48)):
            bucket = get_current_bucket()
            self.assertEqual(bucket, 27)

        with patch(UTC_FN_NAME, make_now_function(hour=23, minute=59)):
            self.assertEqual(get_current_bucket(), 47)

        with patch(UTC_FN_NAME, make_now_function(hour=0, minute=0)):
            self.assertEqual(get_current_bucket(), 0)


    def test_get_bucket_non_dst_zones(self):
        ## Africa/Dar_es_Salaam
        expect = 14
        tz_olson_name = 'Africa/Dar_es_Salaam'
        result = get_today_bucket_for_time('10:00:00', tz_olson_name)
        self.assertEqual(result, expect,
                         "Expected %d for %s, got %d" % (expect, tz_olson_name, result))

        # Argentina/Buenos_Aires
        expect = 26
        tz_olson_name = 'America/Buenos_Aires'
        result = get_today_bucket_for_time('10:00:00', tz_olson_name)
        self.assertEqual(result, expect,
                         "Expected %d for %s, got %d" % (expect, tz_olson_name, result))

        # America/Phoenix
        expect = 34
        tz_olson_name = 'America/Phoenix'
        result = get_today_bucket_for_time('10:00:00', tz_olson_name)
        self.assertEqual(result, expect,
                         "Expected %d for %s, got %d" % (expect, tz_olson_name, result))

        # Asia/Saigon
        expect = 6
        tz_olson_name = 'Asia/Saigon'
        result = get_today_bucket_for_time('10:00:00', tz_olson_name)
        self.assertEqual(result, expect,
                         "Expected %d for %s, got %d" % (expect, tz_olson_name, result))


    def test_get_bucket_non_dst_weird_zones(self):
        """
        no DST but non-even minutes
        """

        # Asia/Katmandu		+05:45	+05:45
        expect = 8
        tz_olson_name = 'Asia/Katmandu'
        result = get_today_bucket_for_time('10:00:00', tz_olson_name)
        self.assertEqual(result, expect,
                         "Expected %d for %s, got %d" % (expect, tz_olson_name, result))


        # Asia/Calcutta		+05:30	+05:30
        expect = 9
        tz_olson_name = 'Asia/Calcutta'
        result = get_today_bucket_for_time('10:00:00', tz_olson_name)
        
        self.assertEqual(result, expect,
                         "Expected %d for %s, got %d" % (expect, tz_olson_name, result))

        # Pacific/Marquesas
        expect = 39
        tz_olson_name = 'Pacific/Marquesas'

        result = get_today_bucket_for_time('10:00:00', tz_olson_name)
        
        self.assertEqual(result, expect,
                         "Expected %d for %s, got %d" % (expect, tz_olson_name, result))


    def test_get_bucket_summerwinter_dst_zones(self):
        # America/Resolute
        #June
        with patch(UTC_FN_NAME, make_now_function(month=6, day=15)):
            expect = 32
            tz_olson_name = 'America/Denver'
            result = get_today_bucket_for_time('10:00:00', tz_olson_name)
            self.assertEqual(result, expect,
                             "Expected %d for %s, got %d" % (expect, tz_olson_name, result))

        #December
        with patch(UTC_FN_NAME, make_now_function(month=12, day=15)):
            expect = 34
            tz_olson_name = 'America/Denver'
            result = get_today_bucket_for_time('10:00:00', tz_olson_name)
            self.assertEqual(result, expect,
                             "Expected %d for %s, got %d" % (expect, tz_olson_name, result))

        #specified_local_noon_dt = datetime.combine(date(2013, 6, 15), time(12, 0, 0, 0, tzinfo=tz))
        #recip.get_local_noon_dt = Mock(return_value=specified_local_noon_dt)
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
