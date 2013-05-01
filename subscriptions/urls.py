from django.conf.urls import patterns, include, url

from .views import TumblrSubscriptionCreateView, SubscriptionDetailView, GenericSubscriptionListView, \
    SubscriptionDeleteView

urlpatterns = patterns('',
    (r'^create/tumblr', TumblrSubscriptionCreateView.as_view()),
    (r'^list', GenericSubscriptionListView.as_view()),
    (r'^detail/tumblr/(?P<pk>\d+)/$', SubscriptionDetailView.as_view()),
    (r'^delete/tumblr/(?P<pk>\d+)/$', SubscriptionDeleteView.as_view()),
)
