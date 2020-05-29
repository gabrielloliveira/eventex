from django.test import TestCase
from django.urls import reverse

from eventex.subscriptions.models import Subscription


class SubscriptionThanksGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(
            name="Gabriell Oliveira",
            email="gabrielloliveira097@gmail.com",
            cpf="12345678901",
            phone="99-99999-9999"
        )
        self.response = self.client.get(reverse("subscriptions:thanks", kwargs={'id': self.obj.id}))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, "subscriptions/thanks.html")

    def test_context(self):
        subscription = self.response.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = [self.obj.name, self.obj.cpf, self.obj.email, self.obj.phone]
        for expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected)


class SubscriptionThanksNotFound(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("subscriptions:thanks", kwargs={'id': 0}))

    def test_not_found(self):
        self.assertEqual(404, self.response.status_code)
