from unittest import mock

from django.contrib.admin.sites import AdminSite

from passit.subject.admin import (
    FieldOfStudyOfAgeGroupAdmin,
    SubjectAdmin,
    SubjectOfAgeGroupAdmin,
)
from passit.subject.models import FieldOfStudyOfAgeGroup, Subject, SubjectOfAgeGroup


class TestSubjectOfAgeGroupAdmin:
    def setup_method(self):
        self.admin = SubjectOfAgeGroupAdmin(
            model=SubjectOfAgeGroup, admin_site=AdminSite()
        )

    def test_get_queryset_select_related(self):
        m_request = mock.Mock()
        queryset = self.admin.get_queryset(m_request)
        assert queryset.query.select_related.get("field_age_group") is not None
        assert (
            queryset.query.select_related["field_age_group"].get("field_of_study")
            is not None
        )


class TestFieldOfStudyOfAgeGroupAdmin:
    def setup_method(self):
        self.admin = FieldOfStudyOfAgeGroupAdmin(
            model=FieldOfStudyOfAgeGroup, admin_site=AdminSite()
        )

    def test_get_queryset_select_related(self):
        m_request = mock.Mock()
        queryset = self.admin.get_queryset(m_request)
        assert queryset.query.select_related.get("field_of_study") is not None


class TestSubjectAdmin:
    def setup_method(self):
        self.admin = SubjectAdmin(model=Subject, admin_site=AdminSite())

    def test_get_queryset_select_related(self):
        m_request = mock.Mock()
        queryset = self.admin.get_queryset(m_request)
        assert queryset.query.select_related.get("field_of_study") is not None
