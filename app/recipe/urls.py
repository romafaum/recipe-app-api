from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views

router = DefaultRouter()
router.register('', views.RecipeViewSet, basename='recipe')

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
