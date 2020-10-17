from typing import TYPE_CHECKING

from django.db.models import Manager, QuerySet

from .querysets import (
    SubjectQuerySet,
    SubjectOfAgeGroupQuerySet,
    FieldOfStudyOfAgeGroupQuerySet,
    FieldOfStudyQuerySet,
    ResourceQuerySet,
)

if TYPE_CHECKING:
    from .models import (
        Subject,
        SubjectOfAgeGroup,
        FieldOfStudy,
        FieldOfStudyOfAgeGroup,
        Resource,
    )
    from ..accounts.models import UserProfile


class FieldOfStudyManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[FieldOfStudy]':
        return FieldOfStudyQuerySet(self.model, self._db)  # type: ignore

    def get_default_by_profile(self, profile: 'UserProfile') -> 'FieldOfStudy':
        return self.get_queryset().get(
            field_age_groups__memberships__profile=profile,
            field_age_groups__memberships__is_default=True,
        )


class FieldOfStudyOfAgeGroupManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[FieldOfStudyOfAgeGroup]':
        return FieldOfStudyOfAgeGroupQuerySet(self.model, self._db)  # type: ignore

    def get_default_by_profile(self, profile: 'UserProfile'):
        return super().get_queryset().get(memberships__profile=profile, memberships__is_default=True)


class SubjectManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[Subject]':
        return SubjectQuerySet(self.model, self._db)  # type: ignore


class SubjectOfAgeGroupManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[SubjectOfAgeGroup]':
        return SubjectOfAgeGroupQuerySet(self.model, self._db)  # type: ignore


class ResourceManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[Resource]':
        return ResourceQuerySet(self.model, self._db)  # type: ignore
