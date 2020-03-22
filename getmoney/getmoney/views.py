from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from .serializers import AdvSerializer, UserSerializer, TokenSerializer
from .models import Adv
from django.contrib.auth.models import User
from rest_framework_simplejwt import views as jwt_views
from rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.models import TokenUser
from getsomemoney import settings


class CustomAccessTokenView(jwt_views.TokenObtainPairView):
    serializer_class = TokenSerializer


class AdvViewSet(viewsets.ModelViewSet):
    queryset = Adv.objects.all()
    serializer_class = AdvSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = [filters.SearchFilter]
    search_fields = ['wn8', 'wins_percent']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)


class MyRegisterView(RegisterView):
    token_model = TokenUser

    def get_response_data(self, user):
        refresh = TokenSerializer.get_token(user)
        data = dict()

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = {"pk": refresh.user.pk,
                        "username": str(refresh.user.username),
                        "email": str(refresh.user.email),
                        "first_name": str(refresh.user.first_name),
                        "last_name": str(refresh.user.last_name)
                        }

        return data

