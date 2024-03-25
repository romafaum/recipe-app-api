from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test1@example.com'
        password = "Testpass123"
        user = get_user_model().objects.create_user(email=email,password=password) # noqa
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalisation(self):
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email, password='Sample123') # noqa
            self.assertEqual(user.email, expected)

    def test_new_user_raise_error_no_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='Sample123') # noqa

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test1@example.com',
            'Password123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
