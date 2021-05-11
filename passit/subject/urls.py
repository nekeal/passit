from typing import Any, List

from rest_framework.routers import DefaultRouter

from .views import (
    FieldOfStudiesViewSet,
    ResourceViewSet,
    SubjectOfAgeGroupViewSet,
    SubjectViewSet,
)

router = DefaultRouter()

router.register("fieldsofstudy", FieldOfStudiesViewSet)
router.register("subjects", SubjectViewSet)
router.register(
    "subjectsagegroup", SubjectOfAgeGroupViewSet, basename="subjects_age_group"
)
router.register("resources", ResourceViewSet)

urlpatterns: List[Any] = []
urlpatterns += router.urls
