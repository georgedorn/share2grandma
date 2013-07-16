from datetime import datetime

from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin

from .models import TumblrSubscription, GenericSubscription, Recipient, Vacation
from .forms import TumblrSubscriptionForm, RecipientForm, VacationForm

from django.shortcuts import get_object_or_404
from subscriptions.models import Recipient

# http://stackoverflow.com/questions/5773724/how-do-i-use-createview-with-a-modelform
class TumblrSubscriptionCreateView(LoginRequiredMixin, CreateView):
    model = TumblrSubscription
    form_class = TumblrSubscriptionForm


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient


class SubscriptionDetailView(LoginRequiredMixin, DetailView):
    model = TumblrSubscription


class GenericSubscriptionListView(LoginRequiredMixin, ListView):
    queryset = GenericSubscription.objects.all()
#    queryset = Book.objects.filter(publisher__name="Acme Publishing")
#    template_name = "books/acme_list.html"


class SubscriptionDeleteView(LoginRequiredMixin, DeleteView):
    model = TumblrSubscription
    success_url = reverse_lazy('subscription_list')

class VacationCreateView(LoginRequiredMixin, CreateView):
    model = Vacation
    form_class = VacationForm
    success_url = reverse_lazy('dashboard_main')
    
    def get_recipient(self):
        """
        Retrieves a recipient given the recipient_id from the url
        and the currently-logged-in user.
        
        Attempting to access a grandmother that doesn't belong to you
        is a 404.
        """
        if not hasattr(self, '_recipient'):
            recipient_id = self.kwargs['recipient_id']
            user = self.request.user
            self._recipient = get_object_or_404(Recipient, pk=recipient_id, user=user)
        return self._recipient
    
    def form_valid(self, form):
        #ensures user is creating a vacation only for their own grandmas:
        form.instance.recipient = self.get_recipient()
        return super(VacationCreateView, self).form_valid(form)
    
    def get_context_data(self, *args, **kwargs):
        context = super(VacationCreateView, self).get_context_data(*args, **kwargs)
        recipient = self.get_recipient()
        context['recipient'] = recipient
        context['timezone_simple'] = recipient.timezone.tzname(datetime.now(), is_dst=False)
        
        return context
    
class VacationDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacation
    success_url = reverse_lazy('dashboard_main')
        
    
    
    
