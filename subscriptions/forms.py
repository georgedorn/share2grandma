from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.shortcuts import get_object_or_404

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
    start_date = forms.DateField(widget=AdminDateWidget())
    end_date = forms.DateField(widget=AdminDateWidget())

    class Meta:
        model = Vacation
        fields = ['start_date', 'end_date']
