from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('', views.UserView.as_view(
        {'get': 'retrieve', 'post': 'create', 'patch': 'partial_update'}),
        name='user'
    ),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
