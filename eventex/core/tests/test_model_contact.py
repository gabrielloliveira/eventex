from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name="Gabriell Oliveira",
            slug="gabriell-oliveira",
            photo="https://ohmycode.com.br/static/img/gabriell.c608c3362dfd.jpeg"
        )

    def test_email(self):
        Contact.objects.create(speaker=self.speaker, kind=Contact.EMAIL,
                               value='gabrielloliveira097@gmail.com')
        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        Contact.objects.create(speaker=self.speaker, kind=Contact.PHONE, value='99-99999-9999')
        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contact king should be limited to E or P"""
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker, kind=Contact.EMAIL, value='gabrielloliveira097@gmail.com')
        self.assertEqual('gabrielloliveira097@gmail.com', str(contact))


class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name="Gabriell Oliveira",
            slug="gabriell-oliveira",
            photo="https://ohmycode.com.br/static/img/gabriell.c608c3362dfd.jpeg"
        )
        s.contact_set.create(kind=Contact.EMAIL, value="gabrielloliveira097@gmail.com")
        s.contact_set.create(kind=Contact.PHONE, value="99-99999-9999")

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['gabrielloliveira097@gmail.com']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phones(self):
        qs = Contact.objects.phones()
        expected = ['99-99999-9999']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)
