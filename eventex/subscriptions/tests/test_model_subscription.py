from datetime import datetime

from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):

    def setUp(self):
        self.obj = Subscription(
            name='Alexandre Menezes',
            cpf='123456789',
            email='amenezes@gmail.com',
            phone='61-11111-1111'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_createt_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)
