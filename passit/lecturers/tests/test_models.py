import pytest

from passit.lecturers.factories import (
    LecturerFactory,
    LecturerOfSubjectOfAgeGroupFactory,
)
from passit.lecturers.models import LecturerOfSubjectOfAgeGroup
from passit.subject.factories import SubjectOfAgeGroupFactory


class TestLecturerOfSubjectQuerySet:
    @pytest.mark.django_db
    def test_annotate_students_start_year(self):
        expected_students_start_year = (
            LecturerOfSubjectOfAgeGroupFactory().subject_group.field_age_group.students_start_year
        )
        lecturer_of_age_group = (
            LecturerOfSubjectOfAgeGroup.objects.annotate_students_start_year().get()
        )
        assert lecturer_of_age_group.students_start_year == expected_students_start_year


class TestLecturerModel:
    def test_lecturer_str_method(self):
        lecturer = LecturerFactory.build(first_name='first_name', last_name='last_name')
        assert str(lecturer) == 'first_name last_name'


class TestLecturerOfSubjectOfAgeGroupModel:
    @pytest.mark.parametrize(
        'lecturer,subject_group,expected',
        (
            (
                LecturerFactory.build(first_name='first_name', last_name='last_name'),
                SubjectOfAgeGroupFactory.build(),
                'first_name last_name subject0',
            ),
        ),
    )
    def test_str_method(self, lecturer, subject_group, expected):
        lecturer_of_age_group = LecturerOfSubjectOfAgeGroupFactory.build(
            lecturer=lecturer, subject_group=subject_group
        )
        assert str(lecturer_of_age_group).startswith(expected)
