from typing import TYPE_CHECKING

from django.db.models import Manager, QuerySet

from .querysets import SubjectQuerySet, SubjectOfAgeGroupQuerySet, FieldOfStudyOfAgeGroupQuerySet, \
    FieldOfStudyQuerySet, ResourceQuerySet
from ..accounts.models import Membership

if TYPE_CHECKING:
    from .models import Subject, SubjectOfAgeGroup, FieldOfStudy, FieldOfStudyOfAgeGroup, Resource
    from ..accounts.models import UserProfile


class FieldOfStudyManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[FieldOfStudy]':
        return FieldOfStudyQuerySet(self.model, self._db)  # type: ignore


class FieldOfStudyOfAgeGroupManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[FieldOfStudyOfAgeGroup]':
        return FieldOfStudyOfAgeGroupQuerySet(self.model, self._db)  # type: ignore

    def filter_by_profile(self, profile: 'UserProfile') -> 'QuerySet[FieldOfStudyOfAgeGroup]':
        field_age_groups_ids = Membership.objects.filter(profile=profile).values('field_age_group')
        return self.get_queryset().filter(id__in=field_age_groups_ids)


class SubjectManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[Subject]':
        return SubjectQuerySet(self.model, self._db)  # type: ignore


class SubjectOfAgeGroupManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[SubjectOfAgeGroup]':
        return SubjectOfAgeGroupQuerySet(self.model, self._db)  # type: ignore


class ResourceManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[Resource]':
        return ResourceQuerySet(self.model, self._db)  # type: ignore
