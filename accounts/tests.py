from django.test import TestCase
from django.contrib.auth import get_user_model

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
        #self.assertEqual(user.password,'ik98')
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


