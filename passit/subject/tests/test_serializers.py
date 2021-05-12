from unittest import mock

import pytest
from rest_framework.fields import Field

from ...accounts.factories import UserProfileFactory
from ..managers import FieldOfStudyOfAgeGroupManager
from ..serializers import (
    FieldAgeGroupDefault,
    FieldAgeGroupRelatedField,
    FieldOfStudyOfAgeGroupSerializer,
    ResourceBaseSerializer,
    SubjectSyllabusImportSerializer,
)


class TestFieldOfAgeGroupSerializer:
    def test_can_serialize_field_age_group(self, field_age_group, field_age_group_data):
        serializer = FieldOfStudyOfAgeGroupSerializer(field_age_group)
        assert serializer.data == {
            "id": field_age_group.id,
            "field_of_study": field_age_group.field_of_study.id,
            "students_start_year": 2018,
        }

    @pytest.mark.django_db
    def test_can_create_field_age_group(self, field_age_group_data):
        serializer = FieldOfStudyOfAgeGroupSerializer(data=field_age_group_data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        assert (instance.field_of_study.id, instance.students_start_year) == (
            field_age_group_data["field_of_study"],
            field_age_group_data["students_start_year"],
        )


class TestResourceSerializer:
    def test_resource_owned_model_serializer(
        self, resource_data, api_rf, user_profile1, user_profile2
    ):
        request_user1 = mock.MagicMock()
        request_user1.user = user_profile1.user
        request_user2 = mock.MagicMock()
        request_user2.user = user_profile2.user
        serializer = ResourceBaseSerializer(
            data=resource_data, context={"request": request_user1}
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        assert instance.created_by == user_profile1, "Creator is set on instace"
        assert instance.modified_by == user_profile1, "Modifier is set on instance"
        serializer = ResourceBaseSerializer(
            data=resource_data, instance=instance, context={"request": request_user2}
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        assert instance.created_by == user_profile1, "Creator is unchanged on instance"
        assert instance.modified_by == user_profile2, "Modifier is changed on instance"


class TestFieldAgeGroupRelatedField:
    @pytest.mark.parametrize(
        ("request1", "user3", "profile3"),
        (
            (None, None, None),
            (mock.Mock(), None, None),
            (mock.Mock(), mock.Mock(), None),
        ),
    )
    def test_get_queryset_without_user_profile_on_request(
        self, monkeypatch, request1, user3, profile3
    ):
        if request1:
            request1.user = user3
            if request1.user:
                request1.user.profile = profile3
        context = {"request": request1}
        serializer = FieldAgeGroupRelatedField()
        serializer._context = context
        queryset = serializer.get_queryset()
        assert not queryset.query.where

    @pytest.mark.django_db
    def test_get_queryset_with_user_profile_on_request(
        self, monkeypatch, student1, field_age_group
    ):
        m_request = mock.Mock()
        m_request.user.profile = student1
        serializer = FieldAgeGroupRelatedField()
        serializer._context = {"request": m_request}
        queryset = serializer.get_queryset()
        assert queryset.query.where.children[0].lookup_name == "in"


class TestFieldAgeGroupDefault:
    def test_call_on_default_returns_field_age_group(self, monkeypatch):
        profile = UserProfileFactory.build()
        m_context = mock.MagicMock()
        m_context["request"].user = profile.user
        m_field_age_group = mock.Mock()
        field = Field()
        field.root._context = m_context
        monkeypatch.setattr(
            FieldOfStudyOfAgeGroupManager,
            "get_default_by_profile",
            mock.Mock(return_value=m_field_age_group),
        )
        default = FieldAgeGroupDefault()
        assert default.requires_context
        assert default(field) == m_field_age_group


class TestSubjectSyllabusImportSerializer:
    @staticmethod
    def get_valid_data(**kwargs):
        valid_data = {
            "name": "subject",
            "semester": 1,
            "general_description": "programming",
            "module_code": "5bFjkWEasNNP",
            "category": "default",
            "field_of_study": kwargs.pop("field_of_study"),
        }
        valid_data.update(kwargs)
        return valid_data

    def test_serializer_can_create_subject(self, field_of_study):
        data = self.get_valid_data(field_of_study=field_of_study.pk)
        serializer = SubjectSyllabusImportSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.save()

        assert subject.name == "subject"
        assert subject.semester == 1
        assert subject.general_description == "programming"
        assert subject.module_code == "5bFjkWEasNNP"
        assert subject.category == "default"
        assert subject.field_of_study == field_of_study
