from datetime import datetime
from sanetime import time, delta
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from subscriptions.models import Recipient, DailyWakeupSubscription,\
    TumblrSubscription
from django.db.models.query_utils import Q


#1. get list of recipients that need to have content pulled at this time
#2. for each of the recipients, get all of their subscriptions
#3. for each of the recipients' subscriptions, call subscription.pull_content()
#4. dispatch the content to the recipient's email address


def get_current_bucket():
    """
    Returns the current bucket based on UTC time.

    Return:
        int. 0-47, where each int represents a ~30min span starting at midnight.
    """
    now = time(datetime.utcnow())
    if now.minute < 30:
        odd_bucket = 0
    else:
        odd_bucket = 1

    return (now.hour * 2) + odd_bucket


class Command(BaseCommand):
    help = """By default, pulls and immediately dispatches longform content and queues
Daily Wakeup content.  All Daily Wakeup content that should be delivered for
the current bucket will also be dispatched unless this switch is invoked."""
    args = ''
    option_list = BaseCommand.option_list + (
        make_option('--no-dispatch-daily-wakeup', default=True,
                    action='store_false', dest='do_daily_wakeup',
                    help="Do not dispatch all Daily Wakeup content queued for current bucket."),
    )

    def handle(self, *args, **options):
        bucket = get_current_bucket()
        #also include recipients that have a daily wakeup subscription 30-90 minutes from now
        recipients = Recipient.get_recipients_due_for_pull(bucket, daily_wakeup_bucket)
        
        #do all of the tumblrs.
        tumblr_subscriptions = TumblrSubscription.objects.filter(recipient__in=recipients)
        
        for tumblr_subscription in tumblr_subscriptions:
            tumblr_subscription.pull_content()

        