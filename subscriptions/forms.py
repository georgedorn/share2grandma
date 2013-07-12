from django.forms import ModelForm
from .models import TumblrSubscription, Recipient

class TumblrSubscriptionForm(ModelForm):
    class Meta:
        model = TumblrSubscription
        exclude = ('pretty_name', 'avatar', 'last_post_ts')     # user can't twiddle these


class RecipientForm(ModelForm):
    class Meta:
        model = Recipient
        exclude = ('add_date',)     # user can't twiddle these
