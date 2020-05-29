from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(
            name='Gabriell Oliveira',
            cpf='12345678901',
            email='gabrielloliveira097@gmail.com',
            phone='99-99999-9999'
        )

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attribute."""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Gabriell Oliveira', str(self.obj))
