import pytest
from django.db.models import F
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate

from ..models import Event
from ..querysets import EventQuerySet
from ..views import EventViewSet
from ...common.utils import setup_view, get_mocked_queryset


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
        monkeypatch.setattr(Event, "objects", m_queryset)
        request = api_rf.get("/api/events/", data={"expand": expand_field_name})
        view = setup_view(EventViewSet(), request)
        view.get_queryset()
        getattr(m_queryset, queryset_method).assert_called_with(
            *queryset_args, **queryset_kwargs
        )
        assert (
            "created_by__user",
            "modified_by__user",
        ) in m_queryset.select_related.call_args_list[0]

    def test_queryset_is_correctly_ordered(self, api_rf, monkeypatch):
        expected_ordering = ("due_date",)
        request = api_rf.get("/api/events")
        view = setup_view(EventViewSet(), request)
        monkeypatch.setattr(Event, "objects", EventQuerySet().none())
        queryset = view.get_queryset()
        assert queryset.query.order_by == expected_ordering

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
