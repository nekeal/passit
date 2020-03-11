import pytest

from teleagh.lecturers.factories import LecturerOfSubjectOfAgeGroupFactory
from teleagh.lecturers.models import LecturerOfSubjectOfAgeGroup


# --- LecturerOfSubjectQuerySet ---


@pytest.mark.django_db
def test_annotate_students_start_year():
    expected_students_start_year = LecturerOfSubjectOfAgeGroupFactory().subject_group.field_age_group.\
        students_start_year
    lecturer_of_age_group = LecturerOfSubjectOfAgeGroup.objects.annotate_students_start_year().get()
    assert lecturer_of_age_group.students_start_year == expected_students_start_year
