from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from .views import TumblrSubscriptionCreateView, SubscriptionDetailView, GenericSubscriptionListView, \
    SubscriptionDeleteView

urlpatterns = patterns('',
    url(r'^create/tumblr', TumblrSubscriptionCreateView.as_view(), name='subscriptions_create_tumblr'),
    url(r'^list', GenericSubscriptionListView.as_view(), name='subscriptions_list'),
    url(r'^detail/tumblr/(?P<pk>\d+)/$', SubscriptionDetailView.as_view(), name='subscriptions_detail_tumblr'),
    url(r'^delete/tumblr/(?P<pk>\d+)/$', SubscriptionDeleteView.as_view(), name='subscriptions_delete_tumblr'),
)
