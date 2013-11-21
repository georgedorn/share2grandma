from django import forms
from django.utils.translation import ugettext as _
from django.contrib.admin.widgets import AdminDateWidget
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import TumblrSubscription, Vacation, Recipient

class TumblrSubscriptionForm(forms.ModelForm):
    class Meta:
        model = TumblrSubscription
        fields = ('recipient', 'enabled', 'short_name')     # whitelist

    def __init__(self, user, *args, **kwargs):
        super(TumblrSubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].queryset = Recipient.objects.filter(sender=user)


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
