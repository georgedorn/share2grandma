from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from .views import TumblrSubscriptionCreateView, SubscriptionDetailView, GenericSubscriptionListView, \
    SubscriptionDeleteView

urlpatterns = patterns('',
    (r'^create/tumblr', login_required(TumblrSubscriptionCreateView.as_view())),
    (r'^list', login_required(GenericSubscriptionListView.as_view())),
    (r'^detail/tumblr/(?P<pk>\d+)/$', login_required(SubscriptionDetailView.as_view())),
    (r'^delete/tumblr/(?P<pk>\d+)/$', login_required(SubscriptionDeleteView.as_view())),
)
