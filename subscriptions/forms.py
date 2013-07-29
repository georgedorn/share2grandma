from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import TumblrSubscription, Vacation, Recipient

class TumblrSubscriptionForm(forms.ModelForm):
    class Meta:
        model = TumblrSubscription
        fields = ('recipient', 'enabled', 'short_name')     # whitelist


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ('user', 'sender_name', 'sender_phone', 'name', 'email', 'timezone')

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
