from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    ROUTES = (
        {
            'template': 'users/login.html',
            'url': '/auth/login/',
        },
        {
            'template': 'users/logged_out.html',
            'url': '/auth/logout/',
        },
        {
            'template': 'users/signup.html',
            'url': '/auth/signup/',
        },
    )

    def test_urls_and_templates_guest(self):
        """URL-адреса используют соответствующие шаблоны."""
        for route in self.ROUTES:
            with self.subTest(url=route['url'], template=route['template']):
                current_client = self.authorized_client
                response = current_client.get(route['url'])
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, route['template'])
