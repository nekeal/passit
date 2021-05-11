from unittest import mock

import pytest

from ...accounts.factories import UserProfileFactory
from ...accounts.models import MembershipQuerySet
from ..factories import EventFactory
from ..models import Event


class TestEventManager:
    @pytest.mark.django_db
    def test_number_of_queries_in_get_by_profile(
        self, monkeypatch, django_assert_num_queries
    ):
        profile = UserProfileFactory.build()
        with django_assert_num_queries(1):
            assert list(Event.objects.get_by_profile(profile)) == []

    @pytest.mark.django_db
    def test_get_by_profile_result(self, monkeypatch):
        monkeypatch.setattr(
            MembershipQuerySet, "values_list", mock.Mock(return_value=[11, 12])
        )
        profile = UserProfileFactory.build()
        expected = {
            EventFactory(field_age_group__id=11),
            EventFactory(field_age_group__id=12),
        }
        EventFactory(field_age_group__id=3)
        assert set(Event.objects.get_by_profile(profile)) == expected


class TestEvent:
    def test_str_method(self):
        expected_result = "event_name"
        assert str(EventFactory.build(name=expected_result)) == expected_result
