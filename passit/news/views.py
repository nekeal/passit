from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..common.permissions import IsPrivilegedOrOwnerOrReadOnly
from .filters import NewsFilterSet
from .models import News
from .serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = (IsAuthenticated, IsPrivilegedOrOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NewsFilterSet

    def get_queryset(self) -> "QuerySet[News]":
        return (
            News.objects.get_by_profile(self.request.user.profile)
            .select_related("created_by__user")
            .select_related("modified_by__user")
            .annotate_is_owner(self.request.user.profile)
            .order_by("-created_at")
        )
