from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .forms import SubscriptionForm


class SubscribeTest(TestCase):
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
        self.assertContains(self.response, "<form")
        self.assertContains(self.response, "<input", 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """HTML must contain csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have SubscriptionForm"""
        form = self.response.context["form"]
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_must_have_fields(self):
        """Form must have 4 fields"""
        form = self.response.context["form"]
        self.assertSequenceEqual(["name", "cpf", "email", "phone"], list(form.fields))


class SubscribePostTest(TestCase):
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

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'gabrielloliveira097@gmail.com']
        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]
        self.assertIn('Gabriell Oliveira', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('gabrielloliveira097@gmail.com', email.body)
        self.assertIn('99-99999-9999', email.body)


class SubscribeInvalidPost(TestCase):
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

