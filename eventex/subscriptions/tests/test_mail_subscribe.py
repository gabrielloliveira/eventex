import unittest

from django.core import mail
from django.test import TestCase
from django.urls import reverse


class SubscribePostValid(TestCase):
    @unittest.skip('Não quero email por agora')
    def setUp(self):
        data = {
            'name': 'Gabriell Oliveira',
            'cpf': '12345678901',
            'email': 'gabrielloliveira097@gmail.com',
            'phone': '99-99999-9999'
        }
        self.response = self.client.post(reverse("subscriptions:subscribe"), data)
        self.email = mail.outbox[0]

    @unittest.skip('Não quero email por agora')
    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    @unittest.skip('Não quero email por agora')
    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    @unittest.skip('Não quero email por agora')
    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'gabrielloliveira097@gmail.com']
        self.assertEqual(expect, self.email.to)

    @unittest.skip('Não quero email por agora')
    def test_subscription_email_body(self):
        contents = ['Gabriell Oliveira', '12345678901', 'gabrielloliveira097@gmail.com', '99-99999-9999']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
