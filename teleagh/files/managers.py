from typing import TYPE_CHECKING

from django.db.models import Manager, QuerySet

from .querysets import FileQuerySet

if TYPE_CHECKING:
    from .models import File


class FileManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[File]':
        return FileQuerySet(self.model, using=self._db)  # type: ignore
