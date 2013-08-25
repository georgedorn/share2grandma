from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from subscriptions.models import Recipient


#1. get list of recipients that need to have content pulled at this time
#2. for each of the recipients, get all of their subscriptions
#3. for each of the recipients' subscriptions, call subscription.pull_content()
#4. dispatch the content to the recipient's email address

def get_current_bucket():
    #@todo:  figure out which bucket the current run belongs to
    return 1

def get_daily_wakeup_bucket():
    now = timezone.now().utcnow()
    now += timezone.timedelta(minutes=30)
    return now.hour
    

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        bucket = get_current_bucket()
        
        recipients = Recipient.objects.filter(bucket=bucket)

        #also include recipients that have a daily wakeup subscription 30-90 minutes from now
        
        
        
        

        
        
        for poll_id in args:
            try:
                poll = Poll.objects.get(pk=int(poll_id))
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write('Successfully closed poll "%s"' % poll_id)