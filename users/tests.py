from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class AdvancedUserTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )

    def test_create_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        self.assertEqual(self.admin_user.username, 'admin')
        self.assertEqual(self.admin_user.email, 'admin@example.com')
        self.assertTrue(self.admin_user.check_password('adminpass'))
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)

    def test_user_str(self):
        self.assertEqual(str(self.user), self.user.username)

    def test_login_user(self):
        login = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login)

    def test_login_superuser(self):
        login = self.client.login(username='admin', password='adminpass')
        self.assertTrue(login)

    def test_password_change(self):
        self.user.set_password('newpass123')
        self.user.save()
        login_old = self.client.login(username='testuser', password='testpass123')
        login_new = self.client.login(username='testuser', password='newpass123')
        self.assertFalse(login_old)
        self.assertTrue(login_new)

    def test_update_user_email(self):
        self.user.email = 'newemail@example.com'
        self.user.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_user_permissions(self):
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)

    def test_user_access_protected_view(self):
        url = reverse('admin:index')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
