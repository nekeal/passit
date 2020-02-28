from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from ..common.permissions import IsPrivilegedOrReadOnly
from .filters import NewsFilterSet
from .models import News
from .serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = (IsPrivilegedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = NewsFilterSet

    def get_queryset(self) -> 'QuerySet[News]':
        return News.objects.get_by_profile(self.request.user.profile)