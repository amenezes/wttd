from unittest.mock import Mock

from django.test import TestCase
from eventex.subscriptions.admin import (
    SubscriptionModelAdmin,
    Subscription,
    admin
)


class SubscriptionModelAdminTest(TestCase):
    def setUp(self):
        Subscription.objects.create(
            name="alexandre menezes",
            cpf='99999999999',
            email='contato@amenezes.dev',
            phone='61-99999999'
        )
        self.queryset = Subscription.objects.all()
        self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)

        mock = Mock()
        old_message_user = SubscriptionModelAdmin.message_user
        SubscriptionModelAdmin.message_user = mock

        self.model_admin.mark_as_paid(None, self.queryset)

        SubscriptionModelAdmin.message_user = old_message_user

    def call_action(self):
        mock = Mock()
        old_message_user = SubscriptionModelAdmin.message_user
        SubscriptionModelAdmin.message_user = mock

        self.model_admin.mark_as_paid(None, self.queryset)

        SubscriptionModelAdmin.message_user = old_message_user
        return mock

    def test_has_action(self):
        self.assertIn('mark_as_paid', self.model_admin.actions)

    def test_mark_all(self):
        self.assertEqual(1, Subscription.objects.filter(paid=True).count())

    def test_message(self):
        mock = self.call_action()
        mock.assert_called_once_with(None, '1 inscrição foi marcada como paga.')