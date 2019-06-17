from django.test import TestCase


class EventexCoreTest(TestCase):

    def setUp(self):
        self.response = self.client.get('/')

    def test_home(self):
        self.assertEqual(200, self.response.status_code)

    def test_eventex_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_subscription_link(self):
        self.assertContains(self.response, 'href="/inscricao/"')