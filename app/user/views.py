from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.seriallizers import UserSerializer, AuthTokenSerializer

# class IsUnAuthenticated(permissions.BasePermission):
#     """
#     Allows access only to unauthenticated users.
#     """

#     def has_permission(self, request, view):
#         user = request.user
#         if user and user.is_authenticated:
#             return False
#         else:
#             return True

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes =[authentication.TokenAuthentication]

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_object(self):
        user = self.request.user
        return user


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES