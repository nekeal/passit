from typing import Any, List

from rest_framework.routers import DefaultRouter

from .views import FileViewSet

router = DefaultRouter()
router.register('files', FileViewSet)

urlpatterns: List[Any] = [

]
