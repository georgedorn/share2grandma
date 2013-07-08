from django.core.urlresolvers import reverse

from django.test import TestCase


class URLRedirectTest(TestCase):

    def test_root_url_redirects_to_dashboard(self):
        res = self.client.get('/', follow=True)
        redir = res.redirect_chain[0]

        self.assertTrue(reverse('dashboard_main') in redir[0])
        self.assertEqual(redir[1], 301)
