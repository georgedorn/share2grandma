from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from .views import TumblrSubscriptionCreateView, SubscriptionDetailView, GenericSubscriptionListView, \
    SubscriptionDeleteView

urlpatterns = patterns('',
    url(r'^create/tumblr', login_required(TumblrSubscriptionCreateView.as_view()), name='subscription_create_tumblr'),
    url(r'^list', login_required(GenericSubscriptionListView.as_view()), name='subscription_list'),
    url(r'^detail/tumblr/(?P<pk>\d+)/$', login_required(SubscriptionDetailView.as_view()), name='subscription_detail_tumblr'),
    url(r'^delete/tumblr/(?P<pk>\d+)/$', login_required(SubscriptionDeleteView.as_view()), name='subscription_delete_tumblr'),
)
