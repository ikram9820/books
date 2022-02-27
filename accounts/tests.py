from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse

from .forms import CustomUserCreationForm
from .views import SignupPageView
class CustomUserTests(TestCase):

    def test_create_user(self):
        User= get_user_model()
        user= User.objects.create_user(
            username='ikram',
            email= 'ik@gmail.com',
            password= 'ik98'
        )
        self.assertEqual(user.username,'ikram')
        self.assertEqual(user.email,'ik@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User= get_user_model()
        admin_user= User.objects.create_superuser(
            username= 'khan',
            email= 'khan@gmail.com',
            password= 'ik98'
        )
        self.assertEqual(admin_user.username,'khan')
        self.assertEqual(admin_user.email,'khan@gmail.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class SingupPageTests(TestCase):
    def setUp(self):
        url= reverse('signup')
        self.response = self.client.get(url)
    
    def test_signup_template(self):
        self.assertEqual(self.response.status_code,200)
        self.assertTemplateUsed(self.response,'registration/signup.html')
        self.assertContains(self.response,'Sign Up')
        self.assertNotContains(self.response,'hi there')

    def test_signup_template(self):
        form= self.response.context.get('form')
        self.assertIsInstance(form,CustomUserCreationForm)
        self.assertContains(self.response,'csrfmiddlewaretoken')

    def test_signup_view(self):
        view= resolve('/accounts/signup/')
        self.assertEqual(view.func.__name__,SignupPageView.as_view().__name__)




















