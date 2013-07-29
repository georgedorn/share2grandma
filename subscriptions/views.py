from datetime import datetime

from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils import timezone

from braces.views import LoginRequiredMixin

from .models import TumblrSubscription, GenericSubscription, Recipient, Vacation
from .forms import TumblrSubscriptionForm, RecipientForm, VacationForm


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
    
    def get_form_kwargs(self):
        """
        Pass the recipient into the VacationForm, to allow access to the recipient's timezone.
        """
        kwargs = super(VacationCreateView, self).get_form_kwargs()
        kwargs['recipient'] = self.get_recipient()
        return kwargs

    
    def form_valid(self, form):
        """
        Override default form_valid to set the recipient
        for the vacation (and 404 if wrong recipient)
        """
        form.instance.recipient = self.get_recipient()
        return super(VacationCreateView, self).form_valid(form)
    
    def get_context_data(self, *args, **kwargs):
        """
        Provide extra vars to the template:
        recipient (from url)
        recipient's timezone as a simple string
        """
        context = super(VacationCreateView, self).get_context_data(*args, **kwargs)
        recipient = self.get_recipient()
        context['recipient'] = recipient
        context['timezone_simple'] = recipient.timezone.tzname(datetime.now(), is_dst=False)
        
        return context
    

class VacationDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacation
    success_url = reverse_lazy('dashboard_main')
    
    def delete(self, request, *args, **kwargs):
        """
        Override the default delete() method to instead set the end_date
        to right now.
        """
        now = timezone.now()

        #get_object takes a queryset, so we're going to pre-filter it to ensure the
        #recipient belongs to the logged-in user
        qs = Vacation.objects.filter(recipient__user=request.user)
        vacation = self.get_object(qs)
        
        if vacation.start_date < now:
            #This vacation has started, so we end it by moving the end date.
            vacation.end_date = now
            vacation.save()
        else:
            #this vacation hasn't started, so we can just delete it.
            vacation.delete()

        return HttpResponseRedirect(self.get_success_url())
    
