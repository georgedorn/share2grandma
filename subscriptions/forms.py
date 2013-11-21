from django import forms
from django.utils.translation import ugettext as _
from django.contrib.admin.widgets import AdminDateWidget
from .models import TumblrSubscription, Vacation, Recipient
from subscriptions.models import TumblrNotFound
from django.core.exceptions import ValidationError

class TumblrSubscriptionForm(forms.ModelForm):
    short_name = forms.CharField(max_length=200, label=_('Tumblr Name or URL'))
    
    class Meta:
        model = TumblrSubscription
        fields = ('recipient', 'short_name')     # whitelist

    def __init__(self, user, *args, **kwargs):
        super(TumblrSubscriptionForm, self).__init__(*args, **kwargs)
        valid_recipients = Recipient.objects.filter(sender=user)
        self.fields['recipient'].queryset = valid_recipients
        self.fields['recipient'].initial = valid_recipients[0]
        self.fields['recipient'].empty_label = None

    def clean_short_name(self):
        """
        Users might specify a tumblr in several ways, so try munging
        them down to the tumblog name.
        
        Also make sure the tumblog exists; this makes a call out to tumblr.
        
        """
        name = self.cleaned_data['short_name']
        name = name.replace('.tumblr.com', '')
        name = name.replace('https://',  '')
        name = name.replace('http://', '')

        
        self.tmp_subscription = TumblrSubscription(short_name=name)
        try:
            self.tmp_subscription.pull_metadata(save=False)
        except TumblrNotFound:
            raise ValidationError("Tumblr %s not found" % self.cleaned_data['short_name'])
        
        return name
    
    def save(self, *args, **kwargs):
        """
        We already pulled metadata for the blog from tumblr during validation.
        
        To avoid a second call during the model's save, copy the results into the instance.
        """
        self.instance.avatar = self.tmp_subscription.avatar
        self.instance.pretty_name = self.tmp_subscription.pretty_name
        self.instance.last_post_ts = self.tmp_subscription.last_post_ts

        return super(TumblrSubscriptionForm, self).save(*args, **kwargs)
    

class RecipientForm(forms.ModelForm):
    """
    Form for creating new Recipients or editing existing ones.
    """
    sender_name = forms.CharField(max_length=40,
                                  label=_('Your name'),
                                  help_text=_('You can customize how this Recipient sees your name.'))

    sender_phone = forms.CharField(max_length=20,
                                   label=_('Your phone'),
                                   help_text=_('Your Recipient will see this phone number at the top of each message.'))

    name = forms.CharField(max_length=40,
                           label=_('Recipient\'s Name'),
                           help_text=_('This is how your Recipient will be displayed on the web site.'))

    email = forms.CharField(max_length=50,
                            label=_('Recipient\'s Presto Email Address'),
                            help_text=_('The email address for your recipient, @presto.com.'))


    class Meta:
        model = Recipient
        fields = ('sender_name', 'sender_phone', 'name', 'email', 'timezone', 'dailywakeup_hour')


class VacationForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=AdminDateWidget())
    end_date = forms.DateTimeField(widget=AdminDateWidget())

    class Meta:
        model = Vacation
        fields = ['start_date', 'end_date']

    def __init__(self, recipient, *args, **kwargs):
        self.recipient = recipient
        return super(VacationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(VacationForm, self).clean()
        start_date = cleaned_data.get('start_date')
        start_date = start_date.replace(tzinfo=self.recipient.timezone)
        end_date = cleaned_data.get('end_date')
        end_date = end_date.replace(tzinfo=self.recipient.timezone)
        if end_date < start_date:
            raise forms.ValidationError("Vacations must start before they end.")
        cleaned_data['start_date'] = start_date
        cleaned_data['end_date'] = end_date
        return cleaned_data
