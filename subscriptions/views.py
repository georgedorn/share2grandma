from datetime import datetime

from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.http.response import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils import timezone

from braces.views import LoginRequiredMixin

from .models import TumblrSubscription, GenericSubscription, Recipient, Vacation
from .forms import TumblrSubscriptionForm, RecipientForm, VacationForm
from django.views.generic.edit import ModelFormMixin, UpdateView
from django.core.exceptions import PermissionDenied


class RecipientMixin(ModelFormMixin):
    form_class = RecipientForm
    model = Recipient

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(RecipientMixin, self).form_valid(form)

    def get_object(self, queryset=None):
        obj = super(RecipientMixin, self).get_object(queryset)
        
        if obj is not None and obj.sender != self.request.user:
            raise PermissionDenied

        return obj
    

class RecipientCreateView(LoginRequiredMixin, RecipientMixin, CreateView):
    pass

class RecipientUpdateView(LoginRequiredMixin, RecipientMixin, UpdateView):
    pass

class RecipientDeleteView(LoginRequiredMixin, RecipientMixin, DeleteView):
    success_url = reverse_lazy('dashboard_main')
    
class RecipientDetailView(LoginRequiredMixin, RecipientMixin, DetailView):
    pass

class TumblrSubscriptionMixin(ModelFormMixin):
    model = TumblrSubscription
    form_class = TumblrSubscriptionForm

    def get_object(self, queryset=None):
        obj = super(TumblrSubscriptionMixin, self).get_object(queryset)
        if obj is not None and obj.recipient.sender != self.request.user:
            raise PermissionDenied
        return obj

    def get_form_kwargs(self):
        kwargs = super(TumblrSubscriptionMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# http://stackoverflow.com/questions/5773724/how-do-i-use-createview-with-a-modelform
class TumblrSubscriptionCreateView(LoginRequiredMixin, TumblrSubscriptionMixin, CreateView):
    pass

class TumblrSubscriptionDetailView(LoginRequiredMixin, TumblrSubscriptionMixin, DetailView):
    pass

class TumblrSubscriptionDeleteView(LoginRequiredMixin, TumblrSubscriptionMixin, DeleteView):
    success_url = reverse_lazy('dashboard_main')


class GenericSubscriptionListView(LoginRequiredMixin, ListView):
    queryset = GenericSubscription.objects.all()

    def get_queryset(self):
        return GenericSubscription.objects.filter(recipient__in=Recipient.objects.filter(sender=self.request.user))


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
            self._recipient = Recipient.objects.get(pk=recipient_id)
            if self._recipient.sender != user:
                raise PermissionDenied
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

    def get_vacation(self, request):
        """
        Returns the vacation associated with the the url;
        also triggers a 404 if the vacation doesn't exist or
        is for a recipient that doesn't belong to the current user.
        """
        qs = Vacation.objects.filter(recipient__sender=request.user)
        vacation = self.get_object(qs)
        return vacation

    def get(self, request, *args, **kwargs):
        """
        Override default get() to do quick permission check.
        """
        self.get_vacation(request)
        return super(VacationDeleteView, self).get(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        """
        Override the default delete() method to instead set the end_date
        to right now.
        """
        now = timezone.now()

        #get_object takes a queryset, so we're going to pre-filter it to ensure the
        #recipient belongs to the logged-in user
        self.object = self.get_vacation(request)
                
        if self.object.start_date < now:
            #This vacation has started, so we end it by moving the end date.
            self.object.end_date = now
            self.object.save()
        else:
            #this vacation hasn't started, so we can just delete it.
            self.object.delete()

        return HttpResponseRedirect(self.get_success_url())