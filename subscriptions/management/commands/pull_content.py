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
    #@todo:  figure out which bucket the current run belongs to
    return 1

def get_daily_wakeup_bucket():
    now = timezone.now().utcnow()
    now += timezone.timedelta(minutes=90) #we do the daily wakeup pulls 90 minutes before delivery deadline
    return now.hour
    

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        bucket = get_current_bucket()
        daily_wakeup_bucket = get_daily_wakeup_bucket()
        #also include recipients that have a daily wakeup subscription 30-90 minutes from now
        recipients = Recipient.get_recipients_due_for_pull(bucket, daily_wakeup_bucket)
        
        #do all of the tumblrs.
        tumblr_subscriptions = TumblrSubscription.objects.filter(recipient__in=recipients)
        
        for tumblr_subscription in tumblr_subscriptions:
            tumblr_subscription.pull_content()

        