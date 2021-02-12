import pytest
from rest_framework import status

from passit.accounts.factories import MembershipFactory
from passit.common.utils import ResponseFactory, setup_view
from passit.subject.factories import FieldOfStudyFactory, SubjectFactory
from passit.subject.views import (
    FieldOfStudiesViewSet,
    SubjectViewSet,
    SubjectOfAgeGroupViewSet, ResourceViewSet,
)


class TestFieldOfStudiesViewSet:
    def test_returns_list_of_field_of_studies_for_student(
        self, student1, django_assert_num_queries
    ):
        with django_assert_num_queries(1):
            response = ResponseFactory(
                "/api/fieldsofstudy/", "get", student1.user
            ).get()
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_fields_of_study_are_filtered_by_user(
        self, student1, field_of_study, django_assert_num_queries
    ):
        FieldOfStudyFactory()
        rf = ResponseFactory("/api/fieldsofstudy/", "get", student1.user)
        with django_assert_num_queries(1):
            response = rf.get()
            qs = setup_view(FieldOfStudiesViewSet(), rf.get_request()).get_queryset()
        assert response.status_code == status.HTTP_200_OK
        assert qs.query.where.children[0].lookup_name == "in"
        assert len(response.data) == 1
        assert response.data[0]['id'] == field_of_study.id


class TestSubjectViewSet:
    def test_returns_list_of_subjects_for_student(
        self, student1, subject, django_assert_num_queries
    ):
        with django_assert_num_queries(1):
            response = ResponseFactory("/api/subjects/", "get", student1.user).get()
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_subjects_are_filtered_by_default_field_of_study(
        self, student1, field_of_study, django_assert_num_queries
    ):
        other_membership = MembershipFactory(is_default=False)
        default_subject = SubjectFactory(field_of_study=field_of_study)
        SubjectFactory(field_of_study=other_membership.field_age_group.field_of_study)
        SubjectFactory()
        rf = ResponseFactory("/api/subjects/", "get", student1.user)
        with django_assert_num_queries(1):
            response = rf.get()
            qs = setup_view(SubjectViewSet(), rf.get_request()).get_queryset()
        assert response.status_code == status.HTTP_200_OK
        assert qs.query.where.children[0].lookup_name == "in"
        assert len(response.data) == 1
        assert response.data[0]['id'] == default_subject.id


class TestSubjectOfAgeGroupViewSet:
    @pytest.mark.parametrize(
        ("query_param", "param_value"),
        (
            ("annotations", "subject_name"),
            ("select_related", "field_age_group"),
        ),
    )
    def test_queryset_when_request_expanded(self, student1, query_param, param_value):
        request = ResponseFactory(
            "/api/subjectsagegroup/",
            "get",
            student1.user,
            {'expand': "field_age_group,subject_name"},
        ).get_request()
        view = setup_view(SubjectOfAgeGroupViewSet(), request)
        qs = view.get_queryset()
        assert qs.query.where.children[0].lookup_name == "in"
        assert getattr(qs.query, query_param).get(param_value) is not None


class TestResourceViewSet:
    @pytest.mark.parametrize(
        ("query_param", "param_value"),
        (
                ("select_related", "subject"),
        ),
    )
    def test_queryset_when_request_expanded(self, student1, query_param, param_value):
        request = ResponseFactory(
            "/api/resources/",
            "get",
            student1.user,
            {'expand': "subject"},
        ).get_request()
        view = setup_view(ResourceViewSet(), request)
        qs = view.get_queryset()
        assert qs.query.where.children[0].lookup_name == "exact"

        assert getattr(qs.query, query_param).get(param_value) is not None
