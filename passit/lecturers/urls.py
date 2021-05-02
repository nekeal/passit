from typing import Any, List

from rest_framework.routers import DefaultRouter

from .views import LecturerViewSet

router = DefaultRouter()

router.register('lecturers', LecturerViewSet)

urlpatterns: List[Any] = []

urlpatterns += router.urls
