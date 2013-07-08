from django.conf.urls import patterns, include, url

from .views import FAQView, DashboardView


urlpatterns = patterns('',
    url(r'^$', DashboardView.as_view(), name='dashboard_main'),
    url(r'^faq/', FAQView.as_view(), name='dashboard_faq'),
)
