from django.urls import reverse
from user.views import profile, profileEdit , logoutPage, loginPage, registerPage
from user.models import Profile
from django.contrib.auth.models import User
from django.test import Client, TestCase

class TestCase(TestCase):

    def setUp(self):
        self.cilent = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.profilePage = reverse('profile')
        self.homePage = reverse('home')
        self.profileForm = reverse('profileEdit')
        self.login = reverse('login')

    def test_profile_GET(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(self.profilePage)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

    def test_home_GET(self):
        response = self.client.get(self.homePage)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_profileForm_GET(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(self.profileForm)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profileEdit.html')

    def test_profileForm_POST(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(self.profileForm, {
            'user': 'john',
            'f_name':'John',
            'l_name':'Heavy',
            'username':'john',
            'email':'lennon@thebeatles.com',
            'age':'22',
            'city':'Guwahati',
            'country':'India',
            'id': 'c1b75889-e930-460d-b697-6eff507dd3d6',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.username, 'john')

    def test_login(self):
        data = {
            'username':'john',
            'password':'johnpassword'
        }
        response = self.client.post(self.login, data, follow=True, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertTemplateUsed(response, 'home.html')

    def test_login_noUsername(self):
        data = {
            'username':'',
            'password':'johnpassword'
        }
        response = self.client.post(self.login, data, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_login_wrong_pass(self):
        data = {
            'username':'john',
            'password':''
        }
        response = self.client.post(self.login, data, format='text/html')
        self.assertEqual(response.status_code, 302)
