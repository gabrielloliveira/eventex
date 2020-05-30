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

    def test_speakers(self):
        """Must show keynote speakers."""
        contents = ["Grace Hopper", "http://hbn.link/hopper-pic",
                    "Alan Turing", "http://hbn.link/turing-pic"]
        for content in contents:
            with self.subTest():
                self.assertContains(self.response, content)

    def test_speaker_link(self):
        expected = f'href="{reverse("core:home")}#speakers"'
        self.assertContains(self.response, expected)
