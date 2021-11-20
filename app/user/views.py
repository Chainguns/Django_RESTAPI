from user.serializers import UserSerialzer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import generics, authentication, permissions

class CreateUserView(generics.CreateAPIView):
    ''' Create a new user in the system '''
    serializer_class = UserSerialzer

class CreateTokenView(ObtainAuthToken):
    """ Creatae a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage the authenticated suer"""

    serializer_class = UserSerialzer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """ Retrieve and return authenticated user"""
        return self.request.user
