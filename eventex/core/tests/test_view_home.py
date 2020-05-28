from django.test import TestCase
from django.urls import reverse


class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use core/index.html"""
        self.assertTemplateUsed(self.response, "core/index.html")

    def test_subsctiprion_link(self):
        link = reverse("subscriptions:subscribe")
        self.assertContains(self.response, f'href="{link}"')
