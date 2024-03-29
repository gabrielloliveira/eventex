import unittest

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("subscriptions:subscribe"))

    def test_get(self):
        """GET 'subscriptions:subscribe' must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, "subscriptions/subscription_form.html")

    def test_html(self):
        """HTML must contain input tags"""
        tags = (
            ('<form', 1),
            ('<input', 6),
            ('type="text', 3),
            ('type="email"', 1),
            ('type="submit"', 1),
        )
        for tag, count in tags:
            with self.subTest():
                self.assertContains(self.response, tag, count)

    def test_csrf(self):
        """HTML must contain csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have SubscriptionForm"""
        form = self.response.context["form"]
        self.assertIsInstance(form, SubscriptionForm)


class SubscriptionsNewPost(TestCase):
    @unittest.skip('Não quer email por agora')
    def setUp(self):
        self.data = {
            'name': 'Gabriell Oliveira',
            'cpf': '12345678901',
            'email': 'gabrielloliveira097@gmail.com',
            'phone': '99-99999-9999'
        }
        self.response = self.client.post(reverse("subscriptions:subscribe"), self.data)

    @unittest.skip('Não quer email por agora')
    def test_post(self):
        """Valid POST should redirect to 'subscriptions:thanks'"""
        subscription = self.response.context['subscription']
        self.assertRedirects(self.response, reverse("subscriptions:thanks", kwargs={'uuid': subscription.uuid}))

    @unittest.skip('Não quer email por agora')
    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewPostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post(reverse("subscriptions:subscribe"), {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertFalse(form.is_valid())

    def test_has_no_subscription(self):
        self.assertFalse(Subscription.objects.exists())


class TemplateRegressionTest(TestCase):
    def test_template_has_no_field_errors(self):
        invalid_data = dict(name="Gabriell Oliveira", cpf="12345678901")
        response = self.client.post(reverse("subscriptions:subscribe"), invalid_data)
        self.assertContains(response, '<ul class="errorlist nonfield">')
