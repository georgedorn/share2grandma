from django.conf.urls import patterns, include, url

from .views import FAQView, TumblrSubscriptionCreateView


urlpatterns = patterns('',
    (r'^faq/', FAQView.as_view()),
    (r'^subscribe/tumblr', TumblrSubscriptionCreateView.as_view()),
)
