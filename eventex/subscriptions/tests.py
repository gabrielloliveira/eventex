from django.test import TestCase
from .forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get("/inscricao/")

    def test_get(self):
        """GET /inscriaco/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, "subscriptions/subscription_form.html")

    def test_html(self):
        """HTML must contain input tags"""
        self.assertContains(self.response, "<form")
        self.assertContains(self.response, "<input", 5)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, '<button>')

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
