from django.test import TestCase
from django.core import mail
from django.shortcuts import resolve_url as r
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionNewGet(TestCase):

    def setUp(self):
        self.response = self.client.get(r('subscriptions:new'))

    def test_get_subscriptions_form(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(
            self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        tags = (
            ('<form', 1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)    


class SubscriptionNewPostValid(TestCase):

    def setUp(self):
        self.data = dict(name='Alexandre Menezes', cpf='123456789', 
                         email='alexandre.fmenezes@gmail.com', 
                         phone='61-99999-9999')
        self.response = self.client.post(r('subscriptions:new'), self.data)
        self.email = mail.outbox[0]

    def test_post(self):
        self.assertRedirects(self.response, r('subscriptions:detail', 1))

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionNewPostInvalid(TestCase):

    def setUp(self):
        self.response = self.client.post(r('subscriptions:new'), {})
        self.form = self.response.context['form']

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(
            self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_errors(self):
        self.assertTrue(self.form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())
