from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views

router = DefaultRouter()
router.register('recipe', views.RecipeViewSet, basename='recipe')
router.register('tags', views.TagViewSet, 'tags')

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
