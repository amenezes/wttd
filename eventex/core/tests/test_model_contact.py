from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.core.exceptions import ValidationError

from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Grace Hopper',
            slug='grace-hopper',
            photo='http://hbn.link/hopper-pic',
            website='http://hbn.link/hopper-site',
            description='Programadora e almirante.'
        )

    def test_email(self):
        contacts = Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.EMAIL,
            value='grace@hopper.io'
        )
        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contacts = Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.PHONE,
            value='61-99999999'
        )
        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        contact = Contact(
            speaker=self.speaker,
            kind='a',
            value='b'
        )
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(
            speaker=self.speaker,
            kind=Contact.EMAIL,
            value='grace@hopper.io'
        )
        self.assertEqual('grace@hopper.io', str(contact))


class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name='Henrique Bastos',
            slug='henrique-bastos',
            photo='http://hbn.link/hb-pic'
        )

        s.contact_set.create(
            kind=Contact.EMAIL,
            value='henrique@bastos.net'
        )
        s.contact_set.create(
            kind=Contact.PHONE,
            value='61-99999999'
        )

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['henrique@bastos.net']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phones(self):
        qs = Contact.objects.phones()
        expected = ['61-99999999']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)