from collections import OrderedDict

from social_auth.db.django_models import UserSocialAuth
from django.views.generic import ListView
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

#@todo: move to settings after pull_content_refactor merged.
AUTH_SERVICES = OrderedDict(
                            [
                             ('tumblr',{'name':'Tumblr'}),
                             ('google-oauth2',{'name':'Google Accounts'}),
                             ('s2g', {'name':'Share2Grandma'}),
                            ]
                           )

AUTH_SERVICES['s2g']['connect_url'] = reverse_lazy('login')
AUTH_SERVICES['s2g']['disconnect_url'] = reverse_lazy("django.contrib.auth.views.logout")

for key in AUTH_SERVICES:
    if 'connect_url' not in AUTH_SERVICES[key]:
        connect_url = reverse_lazy('socialauth_begin', kwargs={'backend':key})
        AUTH_SERVICES[key]['connect_url'] = connect_url
    if 'disconnect_url' not in AUTH_SERVICES[key]:
        disconnect_url = reverse_lazy('socialauth_disconnect', kwargs={'backend':key})
        AUTH_SERVICES[key]['disconnect_url'] = disconnect_url
        

class ServicesListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        """
        Gets all of the currently-logged-in user's social auth connections.
        """
        user = self.request.user
        return user.social_auth.all()
    
    def get_context_data(self, *args, **kwargs):
        context = super(ServicesListView, self).get_context_data(*args, **kwargs)
        logged_in_accounts = context['object_list']
        logged_in_providers = [service.provider for service in logged_in_accounts]
        connected_services = set()

        #User.has_usable_password() returns False if user only registered via social auth services
        if self.request.user.has_usable_password():
            connected_services.add('s2g')
        for service in AUTH_SERVICES:
            if service in logged_in_providers:
                connected_services.add(service)        
        
        context['connected_services'] = connected_services 
        context['all_services'] = AUTH_SERVICES.items()

        return context 
            
        

    

