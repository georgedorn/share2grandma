from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'share2grandma.views.home', name='home'),
    # url(r'^share2grandma/', include('share2grandma.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('dashboard_main'))),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),

    ### 3rd party
    url(r'^social/', include('social_auth.urls')),
    url(r'^registration/', include('registration.backends.default.urls')),

    ### ours
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^subscriptions/', include('subscriptions.urls'))
)
