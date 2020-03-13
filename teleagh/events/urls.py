from typing import Any, List

from rest_framework.routers import DefaultRouter

from .views import EventViewSet

router = DefaultRouter()
router.register('events', EventViewSet)

urlpatterns: List[Any] = [

]


