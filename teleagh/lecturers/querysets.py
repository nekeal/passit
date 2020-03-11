from typing import TYPE_CHECKING

from django.db.models import QuerySet, F

if TYPE_CHECKING:
    from teleagh.lecturers.models import LecturerOfSubjectOfAgeGroup


class LecturerQuerySet(QuerySet):  # type: ignore
    pass


class LecturerOfSubjectQuerySet(QuerySet):  # type: ignore

    def annotate_students_start_year(self, *args, **kwargs) -> 'QuerySet[LecturerOfSubjectOfAgeGroup]':
        return self.annotate(students_start_year=F('subject_group__field_age_group__students_start_year'))
