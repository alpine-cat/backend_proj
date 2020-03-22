from rest_framework import routers
from django.conf.urls import url
from .views import AdvViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'advertisements', AdvViewSet)
