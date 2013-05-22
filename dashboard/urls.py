from django.conf.urls import patterns, include, url

from .views import FAQView, DashboardView


urlpatterns = patterns('',
    (r'^$', DashboardView.as_view()),
    (r'^faq/', FAQView.as_view()),
)
