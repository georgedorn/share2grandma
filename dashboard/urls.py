from django.conf.urls import patterns, include, url

from .views import FAQView


urlpatterns = patterns('',
    (r'^faq/', FAQView.as_view()),
)
