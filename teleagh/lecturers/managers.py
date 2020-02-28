from typing import TYPE_CHECKING

from django.db.models import Manager, QuerySet

from .querysets import LecturerQuerySet

if TYPE_CHECKING:
    from .models import Lecturer, LecturerOfSubject


class LecturerManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[Lecturer]':
        return LecturerQuerySet(self.model, self._db)  # type: ignore


class LecturerOfSubjectManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[LecturerOfSubject]':
        return LecturerQuerySet(self.model, self._db)  # type: ignore