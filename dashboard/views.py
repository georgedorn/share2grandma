from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, CreateView
from braces.views import LoginRequiredMixin

from subscriptions.models import GenericSubscription, TumblrSubscription, TumblrSubscriptionForm


class FAQView(TemplateView):
    template_name = "dashboard/faq.html"


class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"


