from unittest import mock

import pytest
from django.db.models import F
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate

from ...accounts.factories import UserProfileFactory
from ...accounts.models import CustomUser, UserProfile
from ...common.utils import ResponseFactory, get_mocked_queryset, setup_view
from ..managers import EventManager
from ..models import Event
from ..querysets import EventQuerySet
from ..views import EventViewSet


@pytest.fixture
def event_list_view():
    return EventViewSet.as_view({"get": "list", "post": "create"})


class TestEventViewSet:
    @pytest.mark.parametrize(
        "expand_field_name,queryset_method,queryset_args,queryset_kwargs",
        (
            (
                "subject",
                "annotate",
                (),
                {"subject": F("subject_group__subject__name")},
            ),
            (
                "field_age_group",
                "select_related",
                ("field_age_group",),
                {},
            ),
            (
                "subject_group",
                "select_related",
                ("subject_group",),
                {},
            ),
            (
                "subject",
                "select_related",
                ("subject_group__subject",),
                {},
            ),
        ),
    )
    def test_queryset_is_modified_when_fields_are_expanded(
        self,
        monkeypatch,
        api_rf,
        expand_field_name,
        queryset_method,
        queryset_args,
        queryset_kwargs,
    ):
        m_queryset = get_mocked_queryset(EventQuerySet)
        monkeypatch.setattr(
            EventManager, "get_queryset", mock.Mock(return_value=m_queryset)
        )
        monkeypatch.setattr(
            EventManager, "get_by_profile", mock.Mock(return_value=m_queryset)
        )
        request = ResponseFactory(
            "/api/events",
            "get",
            UserProfileFactory.build().user,
            data={"expand": expand_field_name},
        ).get_request()

        view = setup_view(EventViewSet(), request)
        view.get_queryset()

        assert (
            "created_by__user",
            "modified_by__user",
        ) in m_queryset.select_related.call_args_list[0]

        getattr(m_queryset, queryset_method).assert_called_with(
            *queryset_args, **queryset_kwargs
        )

    def test_queryset_is_correctly_ordered(self, api_rf, monkeypatch):
        expected_ordering = ("due_date",)
        request = ResponseFactory(
            "/api/events", "get", UserProfileFactory.build().user
        ).get_request()
        view = setup_view(EventViewSet(), request)
        monkeypatch.setattr(
            EventManager,
            "get_queryset",
            mock.Mock(return_value=EventQuerySet(Event).none()),
        )
        monkeypatch.setattr(
            EventManager,
            "get_by_profile",
            mock.Mock(return_value=EventQuerySet(Event).none()),
        )
        queryset = view.get_queryset()
        assert queryset.query.order_by == expected_ordering

    def test_queryset_if_filtered_by_current_profile(self, monkeypatch):
        profile = mock.Mock(spec=UserProfile)
        user = mock.Mock(spec=CustomUser)
        user.profile = profile
        m_get_by_profile = mock.Mock()
        monkeypatch.setattr(EventManager, "get_by_profile", m_get_by_profile)
        request = ResponseFactory(
            "/api/events/",
            "get",
            user,
        ).get_request()
        view = setup_view(EventViewSet(), request)
        view.get_queryset()
        m_get_by_profile.assert_called_once_with(profile)

    def test_can_create_event_without_subject_group(
        self, event_data, api_rf, event_list_view, user_profile1
    ):
        request = api_rf.post(reverse("api:event-list"), data=event_data)
        force_authenticate(request, user_profile1.user)
        response = event_list_view(request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_can_create_event_with_subject_group(
        self, event_with_subject_group_data, api_rf, event_list_view, user_profile1
    ):
        request = api_rf.post(
            reverse("api:event-list"), data=event_with_subject_group_data
        )
        force_authenticate(request, user_profile1.user)
        response = event_list_view(request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_cant_create_event_without_field_age_group(
        self, event_data, api_rf, event_list_view, user_profile1
    ):
        event_data.pop("field_age_group")
        request = api_rf.post(reverse("api:event-list"), data=event_data)
        force_authenticate(request, user_profile1.user)
        response = event_list_view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("field_age_group"), "field_age_group is required"
