from urllib import response
from django.test import TestCase
from django.urls import reverse

class BaseTest(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.user = {
            'email':'lennon@thebeatles.com',
            'username':'john',
            'passord1':'johnpassword',
            'password2':'johnpassword',
            'first_name':'John',
            'last_name':'Heavy',
        }
        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')

    

