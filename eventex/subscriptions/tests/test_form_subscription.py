from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):

    def make_validate_form(self, **kwargs):
        valid_data = dict(
            name='alexandre menezes',
            cpf='99999999999',
            email='abc@gmail.com',
            phone='61-99999999'
        )
        data = dict(valid_data, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form

    def test_form_has_fields(self):
        form = self.make_validate_form()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        form = self.make_validate_form(cpf='ABCD9999999')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_has_11_digits(self):
        form = self.make_validate_form(cpf='9999')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def test_name_must_be_capitalize(self):
        form = self.make_validate_form(name="ALEX mendes")
        self.assertEqual("Alex Mendes", form.cleaned_data['name'])
