from datetime import datetime

import pytest
import time_machine
from django.core.exceptions import ValidationError

from passit.accounts.factories import MembershipFactory
from passit.subject.factories import (
    FieldOfStudyFactory,
    FieldOfStudyOfAgeGroupFactory,
    SubjectFactory,
    ResourceFactory,
    SubjectOfAgeGroupFactory,
    ExamFactory,
)
from passit.subject.models import (
    FieldOfStudy,
    FieldOfStudyOfAgeGroup,
    year_validator,
    SubjectOfAgeGroup,
    Subject,
    Resource,
)


class TestFieldOfStudyManager:
    def test_get_default_by_profile(
        self, django_assert_num_queries, student1, field_of_study
    ):
        MembershipFactory(profile=student1)
        with django_assert_num_queries(1):
            assert (
                FieldOfStudy.objects.get_default_by_profile(student1) == field_of_study
            )


class TestFieldOfStudyQuerySet:
    def test_filter_by_profile(
        self, django_assert_num_queries, student1, field_of_study
    ):
        FieldOfStudyFactory()

        with django_assert_num_queries(1):
            field_of_study_result = FieldOfStudy.objects.filter_by_profile(
                student1
            ).get()  # only single field of study match

        assert field_of_study_result == field_of_study

    def test_filter_by_profile_with_multiple_memberships(
        self, student1, field_of_study
    ):
        matching_field_age_group = FieldOfStudyOfAgeGroupFactory()
        MembershipFactory(profile=student1, field_age_group=matching_field_age_group)
        FieldOfStudyFactory()
        result = FieldOfStudy.objects.filter_by_profile(student1)

        assert set(result) == {matching_field_age_group.field_of_study, field_of_study}


class TestFieldOfStudy:
    def test_str_method(self):
        field_of_study = FieldOfStudyFactory.build()
        assert str(field_of_study) == field_of_study.name


class TestFieldOfStudyOfAgeGroupManager:
    def test_get_default_by_profile(
        self, django_assert_max_num_queries, student1, field_age_group
    ):
        """
        3 FieldOfStudyOfAgeGroup are created in total
        2 Memberships for student1 are created
        """
        MembershipFactory(profile=student1)
        FieldOfStudyOfAgeGroupFactory()
        with django_assert_max_num_queries(1):
            assert (
                FieldOfStudyOfAgeGroup.objects.get_default_by_profile(student1)
                == field_age_group
            )


class TestFieldOfStudyOfAgeGroup:
    @time_machine.travel(datetime(2020, 1, 1))
    @pytest.mark.parametrize(
        ("year",),
        (
            (2018,),
            (2019,),
            (2020,),
        ),
    )
    def test_validate_valid_year(self, year):
        assert year_validator(year) is None

    @time_machine.travel(datetime(2020, 1, 1))
    @pytest.mark.parametrize(
        ("year",),
        (
            (2017,),
            (2021,),
        ),
    )
    def test_validate_year_raises_error(self, year):
        with pytest.raises(ValidationError):
            year_validator(year)

    def test_str_method(self):
        field_age_group = FieldOfStudyOfAgeGroupFactory.build()
        assert (
            str(field_age_group)
            == f"{field_age_group.field_of_study} {field_age_group.students_start_year}"
        )


class TestSubjectQuerySet:
    def test_filter_by_profile(self, django_assert_num_queries, student1, subject):
        other_membership = MembershipFactory(profile=student1)
        other_subject = SubjectFactory(
            field_of_study=other_membership.field_age_group.field_of_study
        )
        SubjectFactory()
        with django_assert_num_queries(1):
            result = Subject.objects.filter_by_profile(student1)
            assert set(result) == {subject, other_subject}


class TestSubject:
    def test_str_method(self):
        subject = SubjectFactory.build()
        assert str(subject) == subject.name


class TestResourceQuerySet:
    def test_filter_by_profile(self, django_assert_num_queries, student1, resource):
        other_membership = MembershipFactory(profile=student1)
        other_resource = ResourceFactory(
            subject__field_of_study=other_membership.field_age_group.field_of_study
        )
        ResourceFactory()
        with django_assert_num_queries(1):
            result = Resource.objects.filter_by_profile(student1)
            assert len(result) == 2
            assert set(result) == {resource, other_resource}


class TestResource:
    def test_str_method(self):
        resource = ResourceFactory.build()
        assert str(resource) == f"{resource.name} - {resource.subject}"


class TestSubjectOfAgeGroupQuerySet:
    def test_filter_by_profile(self, student1, subject_group):
        SubjectOfAgeGroupFactory()

        result = SubjectOfAgeGroup.objects.filter_by_profile(student1).get()

        assert result == subject_group

    def test_filter_by_profile_with_multiple_membership(self, student1, subject_group):
        other_subject_group = SubjectOfAgeGroupFactory()
        MembershipFactory(
            profile=student1, field_age_group=other_subject_group.field_age_group
        )

        result = SubjectOfAgeGroup.objects.filter_by_profile(student1)

        assert set(result) == {subject_group, other_subject_group}

    def test_add_subject_name(self):
        queryset = SubjectOfAgeGroup.objects.add_subject_name()
        assert queryset.query.annotations.get("subject_name") is not None


class TestSubjectOfAgeGroup:
    def test_str_method(self):
        subject_group = SubjectOfAgeGroupFactory.build()
        assert (
            str(subject_group)
            == f"{subject_group.subject} {subject_group.field_age_group}"
        )


class TestExam:
    def test_str_method(self):
        exam = ExamFactory.build()
        assert str(exam) == f"{exam.subject_group} {exam.starts_at}"
