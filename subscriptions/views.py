from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, CreateView, DetailView

from .models import TumblrSubscription, TumblrSubscriptionForm, GenericSubscription

# http://stackoverflow.com/questions/5773724/how-do-i-use-createview-with-a-modelform
class TumblrSubscriptionCreateView(CreateView):
    model = TumblrSubscription
    form_class = TumblrSubscriptionForm
    #object = None   # cause we're creating a new one

    # get() is provided by CreateView
    # post() is provided by CreateView and, if successful, redirects to the TumblrSubscription object by default


class SubscriptionListView(ListView):
    context_object_name = "subscription_list"
#    queryset = Book.objects.filter(publisher__name="Acme Publishing")
#    template_name = "books/acme_list.html"

class SubscriptionDetailView(DetailView):
    model = TumblrSubscription


class GenericSubscriptionListView(ListView):
# ??    context_object_name = "subscription_list"
    queryset = GenericSubscription.objects.all()
#    queryset = Book.objects.filter(publisher__name="Acme Publishing")
#    template_name = "books/acme_list.html"