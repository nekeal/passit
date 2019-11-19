from typing import List, Any

from rest_framework.routers import DefaultRouter

from lecturers.views import LecturerViewSet

router = DefaultRouter()

router.register('lecturers', LecturerViewSet)

urlpatterns: List[Any] = [

]

urlpatterns += router.urls
