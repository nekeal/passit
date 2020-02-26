import pytest

from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate

from accounts.factories import UserFactory
from accounts.models import UserProfile
from ..managers import NewsManager
from ..models import News
from ..views import NewsViewSet


@pytest.fixture
def news_list_view():
    return NewsViewSet.as_view({'get': 'list', 'post': 'create'})


# --- NeswViewSet ---

@mock.patch.object(NewsManager, 'get_by_profile', return_value=News.objects.none())
def test_news_are_filtered_by_user(m_get_by_profile, api_rf, news_list_view, user_profile, django_assert_num_queries):
    request = api_rf.get(reverse('api:news-list'))
    force_authenticate(request, user_profile.user)
    with django_assert_num_queries(0):  # original query is mocked
        news_list_view(request)
    m_get_by_profile.assert_called_once()


@pytest.mark.parametrize("is_privileged,expected_status", ((True, status.HTTP_200_OK),
                                                           (False, status.HTTP_200_OK)))
def test_user_access_to_list_view(is_privileged, expected_status, user_profile, api_rf, news_list_view, mocker):
    mocker.patch.object(UserProfile, 'is_privileged', return_value=is_privileged)
    request = api_rf.get(reverse('api:news-list'))
    force_authenticate(request, user_profile.user)
    response = news_list_view(request)
    assert response.status_code == expected_status


@pytest.mark.parametrize("is_privileged,expected_status", ((True, status.HTTP_201_CREATED),
                                                           (False, status.HTTP_403_FORBIDDEN)))
def test_user_access_to_create_view(is_privileged, expected_status, user_profile, news_data, api_rf, news_list_view,
                                    mocker):
    mocker.patch.object(UserProfile, 'is_privileged', return_value=is_privileged)
    request = api_rf.post(reverse('api:news-list'), data=news_data)
    force_authenticate(request, user_profile.user)
    response = news_list_view(request)
    assert response.status_code == expected_status
