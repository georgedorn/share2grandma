from django.forms import ModelForm
from .models import TumblrSubscription

class TumblrSubscriptionForm(ModelForm):
    class Meta:
        model = TumblrSubscription
        exclude = ('pretty_name', 'avatar', 'last_post_ts')     # user can't twiddle these
