from django.urls import path, include
from rest_framework.routers import DefaultRouter

from teleagh.accounts.views import CustomUserViewSet

app_name = 'accounts'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include('djoser.urls.jwt')),
]
