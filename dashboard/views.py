from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, CreateView

from subscriptions.models import TumblrSubscription, TumblrSubscriptionForm


class FAQView(TemplateView):
    template_name = "dashboard/faq.html"


# http://stackoverflow.com/questions/5773724/how-do-i-use-createview-with-a-modelform
class TumblrSubscriptionCreateView(CreateView):
    model = TumblrSubscription
    form_class = TumblrSubscriptionForm
    object = None   # cause we're creating a new one
#    template_name = "dashboard/tumblrsubscription_form.html"  # why do i have to specify? i thought this was default

    def get(self, request, *args, **kwargs):
        form = self.form_class()
#        return self.render_to_response(request)
        return render(request, self.get_template_names(), {'form': form})

    def post(self, request):
        return HttpResponse("Post")


class SubscriptionListView(ListView):
    context_object_name = "subscription_list"
#    queryset = Book.objects.filter(publisher__name="Acme Publishing")
#    template_name = "books/acme_list.html"