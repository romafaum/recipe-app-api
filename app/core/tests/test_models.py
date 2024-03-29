from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def create_user(email='testuser@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test1@example.com'
        password = "Testpass123"
        user = create_user(email, password)
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
            user = create_user(email=email, password='Sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_raise_error_no_email(self):
        with self.assertRaises(ValueError):
            create_user(email='', password='Sample123')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test1@example.com',
            'Password123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_recipe(self):
        user = get_user_model().objects.create_superuser(
            'test1@example.com',
            'Password123'
        )
        recipe = models.Recipe.objects.create(
            owner=user,
            title='Sample title',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description.',
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()

        tag = models.Tag(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)
