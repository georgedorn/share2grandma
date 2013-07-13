from django.forms import ModelForm
from .models import TumblrSubscription, Recipient

class TumblrSubscriptionForm(ModelForm):
    class Meta:
        model = TumblrSubscription
        fields = ('recipient', 'enabled', 'short_name')     # whitelist


class RecipientForm(ModelForm):
    class Meta:
        model = Recipient
        exclude = ('add_date',)     # user can't twiddle these
        fields = ('user', 'sender_name', 'sender_phone', 'name', 'add_date', 'email', 'timezone')
