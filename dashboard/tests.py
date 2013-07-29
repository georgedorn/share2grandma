from django.core.urlresolvers import reverse

from django.test import TestCase


class URLRedirectTest(TestCase):

    def test_root_url_redirects_to_dashboard(self):
        res = self.client.get('/', follow=True)
        redir = res.redirect_chain[0]

        self.assertTrue(reverse('dashboard_main') in redir[0])
        self.assertEqual(redir[1], 301)

class LoginRequired(TestCase):
    def test_login_require_dashboard(self):

        pages = [reverse('dashboard_main'), reverse('dashboard_faq')]

        for page in pages:
            res = self.client.get(page, follow=True)

            success = False
            for url, status in res.redirect_chain:
                if reverse('auth_login') in url:
                    if status >= 301 and status <= 302:
                        success = True
            self.assertTrue(success)