from typing import List, Any

from rest_framework.routers import DefaultRouter

from .views import LecturerViewSet

router = DefaultRouter()

router.register('lecturers', LecturerViewSet)

urlpatterns: List[Any] = [

]

urlpatterns += router.urls
