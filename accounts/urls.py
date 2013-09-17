from django.conf.urls import patterns, include, url
from .views import ServicesListView

urlpatterns = patterns('',
    url(r'^list', ServicesListView.as_view(), name='auth_services_list'),
)
