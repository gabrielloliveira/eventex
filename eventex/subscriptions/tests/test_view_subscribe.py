from django.core import mail
from django.test import TestCase
from django.urls import reverse

from eventex.subscriptions.forms import SubscriptionForm


class SubscribeGet(TestCase):
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


class SubscribePostValid(TestCase):
    def setUp(self):
        data = {
            'name': 'Gabriell Oliveira',
            'cpf': '12345678901',
            'email': 'gabrielloliveira097@gmail.com',
            'phone': '99-99999-9999'
        }
        self.response = self.client.post(reverse("subscriptions:subscribe"), data)

    def test_post(self):
        """Valid POST should redirect to 'subscriptions:subscribe'"""
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


class SubscribePostInvalid(TestCase):
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


class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        data = {
            'name': 'Gabriell Oliveira',
            'cpf': '12345678901',
            'email': 'gabrielloliveira097@gmail.com',
            'phone': '99-99999-9999'
        }
        self.response = self.client.post(reverse("subscriptions:subscribe"), data, follow=True)

    def test_message(self):
        self.assertContains(self.response, 'Inscrição realizada com sucesso!')

