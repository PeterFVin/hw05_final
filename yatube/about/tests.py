from http import HTTPStatus

from django.test import Client, TestCase


class PostModelTest(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_urls_and_templates_author(self):
        """Проверка шаблона и доступности адреса /about/author/."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'about/author.html')

    def test_urls_and_templates_tech(self):
        """Проверка шаблона и доступности адреса /about/tech/."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'about/tech.html')
