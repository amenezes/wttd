from django.test import TestCase
from django.core import mail
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionsTests(TestCase):

    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get_subscriptions_form(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):

    def setUp(self):
        self.data = dict(name='Alexandre Menezes', cpf='123456789', 
                         email='alexandre.fmenezes@gmail.com', 
                         phone='61-99999-9999')
        self.response = self.client.post('/inscricao/', self.data)
        self.email = mail.outbox[0]

    def test_post(self):
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

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
        self.assertIn('Alexandre Menezes', self.email.body)
        self.assertIn('123456789', self.email.body)
        self.assertIn('alexandre.fmenezes@gmail.com', self.email.body)
        self.assertIn('61-99999-9999', self.email.body)


class SubscribeInvalidPost(TestCase):

    def setUp(self):
        self.response = self.client.post('/inscricao/', {})
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


class SubscribeSuccessMessage(TestCase):

    def setUp(self):
        self.data = dict(name='Alexandre Menezes', cpf='123456789', 
                         email='alexandre.fmenezes@gmail.com', 
                         phone='61-99999-9999')
        self.response = self.client.post(
            '/inscricao/', self.data, follow=True)

    def test_message(self):
        self.assertContains(
            self.response, "Inscrição realizada com sucesso!")