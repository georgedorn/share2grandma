from django.conf.urls import patterns, include, url

from .views import TumblrSubscriptionCreateView, TumblrSubscriptionDetailView, GenericSubscriptionListView, \
    TumblrSubscriptionDeleteView, RecipientCreateView, RecipientDetailView, VacationCreateView, \
    VacationDeleteView, RecipientDeleteView, RecipientUpdateView

urlpatterns = patterns('',
    url(r'^create/tumblr', TumblrSubscriptionCreateView.as_view(), name='subscription_create_tumblr'),
    url(r'^list', GenericSubscriptionListView.as_view(), name='subscription_list'),
    url(r'^detail/tumblr/(?P<pk>\d+)/$', TumblrSubscriptionDetailView.as_view(), name='subscription_detail_tumblr'),
    url(r'^delete/tumblr/(?P<pk>\d+)/$', TumblrSubscriptionDeleteView.as_view(), name='subscription_delete_tumblr'),
    url(r'^recipient/create', RecipientCreateView.as_view(), name='recipient_create'),
    url(r'^recipient/(?P<pk>\d+)/$', RecipientDetailView.as_view(), name='recipient_detail'),
    url(r'^recipient/(?P<pk>\d+)/delete/$', RecipientDeleteView.as_view(), name='recipient_delete'),
    url(r'^recipient/(?P<pk>\d+)/edit/$', RecipientUpdateView.as_view(), name='recipient_update'),
    url(r'^vacation/create/(?P<recipient_id>\d+)/$', VacationCreateView.as_view(), name='vacation_create'),
    url(r'^vacation/cancel/(?P<pk>\d+)/$', VacationDeleteView.as_view(), name='vacation_cancel'),
)
