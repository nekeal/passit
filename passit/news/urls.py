from typing import Any, List

from rest_framework.routers import DefaultRouter

from passit.news.views import NewsViewSet

router = DefaultRouter()

router.register("news", NewsViewSet, basename="news")

urlpatterns: List[Any] = []

urlpatterns += router.urls
