from django.test import TestCase
from django.core import mail
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):

    def setUp(self):
        self.data = dict(
            name='Alexandre Menezes',
            cpf='12345678900',
            email='alexandre.fmenezes@gmail.com',
            phone='61-99999-9999'
        )
        self.response = self.client.post(r('subscriptions:new'), self.data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = [
            'contato@eventex.com.br',
            'alexandre.fmenezes@gmail.com'
        ]

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Alexandre Menezes',
            '123456789',
            'alexandre.fmenezes@gmail.com',
            '61-99999-9999'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
