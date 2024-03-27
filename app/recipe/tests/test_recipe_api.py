from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def recepi_detail_url(id):
    return reverse('recipe:recipe-detail', args=[id])


def create_user(email, password, name="Test user"):
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        name=name
    )


def create_recipe(user, **params):
    default = {
        'title': 'Some test title',
        'description': 'Some description of the recipe',
        'time_minutes': 60,
        'price': Decimal('10.3'),
        'link': 'exmaple.com/recipe.pdf'
    }
    default.update(params)
    recipe = Recipe.objects.create(owner=user, **default)
    return recipe


class PublicRecipeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unth_request(self):
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user('testuser1@example.com', 'testpass123')
        self.client.force_authenticate(self.user)

    def test_retvire_recipe(self):
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):
        other_user = create_user('otherUser@example.com', 'password123')
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(owner=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recepi_detail(self):
        recipe = create_recipe(user=self.user)

        url = recepi_detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        payload = {
            'title': 'Some test title',
            'description': 'Some description of the recipe',
            'time_minutes': 60,
            'price': Decimal('10.3'),
            'link': 'exmaple.com/recipe.pdf'
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.owner, self.user)

    def test_partial_update(self):
        original_link = 'exmple.com/recipe.pdf'
        recipe = create_recipe(
            user=self.user,
            title='Old title',
            link=original_link
        )
        payload = {'title': 'new title'}
        res = self.client.patch(recepi_detail_url(recipe.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.owner, self.user)

    def test_full_update(self):
        recipe = create_recipe(
            user=self.user,
            title='Some test title',
            description='Some description of the recipe',
            link='exmaple.com/recipe.pdf'
        )

        payload = {
            'title': 'New title',
            'description': 'New description of the recipe',
            'time_minutes': 40,
            'price': Decimal('1.3'),
            'link': 'exmaple.com/new-recipe.pdf'
        }
        url = recepi_detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.owner, self.user)

    def test_update_user_return_error(self):
        new_user = create_user('Lox123@mail.com', 'Passsw123')
        recipe = create_recipe(
            user=self.user,
            title='Some test title',
            description='Some description of the recipe',
            link='exmaple.com/recipe.pdf'
        )
        payload = {'owner': new_user}
        url = recepi_detail_url(recipe.id)
        self.client.put(url, payload)

        recipe.refresh_from_db()

        self.assertEqual(recipe.owner, self.user)

    def test_delete_recepi(self):
        recipe = create_recipe(
            user=self.user,
            title='Some test title'
        )
        url = recepi_detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_other_user_recepi(self):
        new_user = create_user('Lox123@mail.com', 'Passsw123')
        recipe = create_recipe(
            user=new_user,
            title='Some test title',
        )

        url = recepi_detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
