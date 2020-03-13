import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate

from ..views import EventViewSet


# --- EventViewSet ---


@pytest.fixture
def event_list_view():
    return EventViewSet.as_view({'get': 'list', 'post': 'create'})


def test_can_create_event_without_subject_group(event_data, api_rf, event_list_view, user_profile1):
    request = api_rf.post(reverse('api:event-list'), data=event_data)
    force_authenticate(request, user_profile1.user)
    response = event_list_view(request)
    assert response.status_code == status.HTTP_201_CREATED


def test_can_create_event_with_subject_group(event_with_subject_group_data, api_rf, event_list_view, user_profile1):
    request = api_rf.post(reverse('api:event-list'), data=event_with_subject_group_data)
    force_authenticate(request, user_profile1.user)
    response = event_list_view(request)
    assert response.status_code == status.HTTP_201_CREATED


def test_cant_create_event_without_field_age_group(event_data, api_rf, event_list_view, user_profile1):
    event_data.pop('field_age_group')
    request = api_rf.post(reverse('api:event-list'), data=event_data)
    force_authenticate(request, user_profile1.user)
    response = event_list_view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data.get('field_age_group'), 'field_age_group is required'
