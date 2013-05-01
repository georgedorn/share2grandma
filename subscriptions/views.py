from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, CreateView, DetailView

from .models import TumblrSubscription, TumblrSubscriptionForm, GenericSubscription

# http://stackoverflow.com/questions/5773724/how-do-i-use-createview-with-a-modelform
class TumblrSubscriptionCreateView(CreateView):
    model = TumblrSubscription
    form_class = TumblrSubscriptionForm


class SubscriptionDetailView(DetailView):
    model = TumblrSubscription



class GenericSubscriptionListView(ListView):
    queryset = GenericSubscription.objects.all()
#    queryset = Book.objects.filter(publisher__name="Acme Publishing")
#    template_name = "books/acme_list.html"