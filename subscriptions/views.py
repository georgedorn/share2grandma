from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy

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


class SubscriptionDeleteView(DeleteView):
    model = TumblrSubscription
    success_url = reverse_lazy('subscription_list')