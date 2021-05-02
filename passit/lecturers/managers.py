from typing import TYPE_CHECKING

from django.db.models import Manager, QuerySet

from .querysets import LecturerOfSubjectQuerySet, LecturerQuerySet

if TYPE_CHECKING:
    from .models import Lecturer, LecturerOfSubjectOfAgeGroup


class LecturerManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[Lecturer]':
        return LecturerQuerySet(self.model, self._db)  # type: ignore


class LecturerOfSubjectManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[LecturerOfSubjectOfAgeGroup]':
        return LecturerOfSubjectQuerySet(self.model, self._db)  # type: ignore
