from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from subscriptions.models import Recipient, DailyWakeupSubscription,\
    TumblrSubscription

from share2grandma.utils import get_current_bucket

#1. get list of recipients that need to have content pulled at this time
#2. for each of the recipients, get all of their subscriptions
#3. for each of the recipients' subscriptions, call subscription.pull_content()
#4. dispatch the content to the recipient's email address



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
        recipients = Recipient.get_recipients_due_for_processing(bucket)
        
        for recipient in recipients:
            recipient.deliver(bucket)
        
