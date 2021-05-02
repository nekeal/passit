from django.urls import include, path
from rest_framework.routers import DefaultRouter

from passit.accounts.views import CustomUserViewSet

app_name = 'accounts'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include('djoser.urls.jwt')),
]
