from django.core import mail
from django.test import TestCase
from portfolio.core.form import EmailForm


class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'index.html')


class EmailTest(TestCase):
    def setUp(self):
        data = dict(name='Adriano Regis',
                    email='adriano.regis.vidal@outlook.com',
                    phone='+351 966080448',
                    message='Teste de envio.')
        self.resp = self.client.post('/', data)

    def test_post(self):
        """Valid POST should redirect to /email/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_email_subject(self):
        email = mail.outbox[0]
        expect = 'Solicitação de serviços'

        self.assertEqual(expect, email.subject)

    def test_email_from(self):
        email = mail.outbox[0]
        expect = 'adbrumvidal@gmail.com'

        self.assertEqual(expect, email.from_email)

    def test_email_to(self):
        email = mail.outbox[0]
        expect = ['adbrumvidal@gmail.com', 'adriano.regis.vidal@outlook.com']

        self.assertEqual(expect, email.to)

    def test_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Adriano Regis', email.body)
        self.assertIn('adriano.regis.vidal@outlook.com', email.body)
        self.assertIn('+351 966080448', email.body)

class EmailInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'index.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, EmailForm)

    def test_form_has_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class EmailSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Adriano Regis',
                    email='adriano.regis.vidal@outlook.com',
                    phone='+351 966080448',
                    message='Solicitação enviada com sucesso!')
        response = self.client.post('/', data, follow=True)
        self.assertContains(response, 'Solicitação enviada com sucesso!')