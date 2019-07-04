from django.test import TestCase
from django.shortcuts import resolve_url as r

from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(
            name='Alexandre Menezes',
            cpf='99999999999',
            email='alexandre.fmenezes@gmail.com',
            phone='61-9999999'
        )
        self.resp = self.client.get(r('subscriptions:detail', self.obj.pk))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_(self):
        self.assertTemplateUsed(
            self.resp,
            'subscriptions/subscription_detail.html'
        )

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        content = (
            self.obj.name,
            self.obj.cpf,
            self.obj.email,
            self.obj.phone
        )
        with self.subTest():
            for excpected in content:
                self.assertContains(self.resp, excpected)


class SubscriptionDetailNotFound(TestCase):

    def setUp(self):
        self.response = self.client.get(r('subscriptions:detail', 0))

    def test_not_found(self):
        self.assertEqual(404, self.response.status_code)
