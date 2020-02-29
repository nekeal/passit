from typing import List, Any

from rest_framework.routers import DefaultRouter

from teleagh.subject.views import FieldOfStudiesViewSet, SubjectViewSet, ResourceViewSet

router = DefaultRouter()

router.register('fieldsofstudy', FieldOfStudiesViewSet)
router.register('subjects', SubjectViewSet)
router.register('resources', ResourceViewSet)

urlpatterns: List[Any] = [

]
urlpatterns += router.urls
