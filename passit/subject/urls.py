from typing import List, Any

from rest_framework.routers import DefaultRouter

from .views import FieldOfStudiesViewSet, SubjectViewSet, ResourceViewSet, SubjectOfAgeGroupViewSet

router = DefaultRouter()

router.register('fieldsofstudy', FieldOfStudiesViewSet)
router.register('subjects', SubjectViewSet)
router.register('subjectsagegroup', SubjectOfAgeGroupViewSet, basename='subjects_age_group')
router.register('resources', ResourceViewSet)

urlpatterns: List[Any] = [

]
urlpatterns += router.urls
