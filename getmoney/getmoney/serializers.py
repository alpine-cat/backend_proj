from rest_framework import serializers
from .models import Adv
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class AdvSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Adv
        fields = ('url', 'owner', 'datetime_start', 'datetime_end', 'content', 'wn8', 'wins_percent', 'url_clan')


class UserSerializer(serializers.ModelSerializer):
    ads = serializers.PrimaryKeyRelatedField(many=True, queryset=Adv.objects.all())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'ads')


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token.user = User.objects.get(username=user.username)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = {"pk": refresh.user.pk,
        "username": str(refresh.user.username),
        "email": str(refresh.user.email),
        "first_name": str(refresh.user.first_name),
        "last_name": str(refresh.user.last_name)
                         }

        return data


