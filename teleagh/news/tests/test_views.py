from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate

from ..managers import NewsManager
from ..models import News
from ..views import NewsViewSet
from ...accounts.factories import MembershipFactory
from ...common.utils import setup_view
from ...subject.models import FieldOfStudyOfAgeGroup


@pytest.fixture
def news_list_view():
    return NewsViewSet.as_view({'get': 'list', 'post': 'create'})


# --- NeswViewSet ---

@mock.patch.object(NewsManager, 'get_by_profile', return_value=News.objects.none())
def test_news_are_filtered_by_user(m_get_by_profile, api_rf, news_list_view, user_profile1, django_assert_num_queries):
    request = api_rf.get(reverse('api:news-list'))
    force_authenticate(request, user_profile1.user)
    with django_assert_num_queries(0):  # original query is mocked
        news_list_view(request)
    m_get_by_profile.assert_called_once()


def test_news_viewset_get_queryset(api_rf, user_profile1, news_list_view):
    request = api_rf.get('')
    request.user = user_profile1.user
    view_instance = setup_view(NewsViewSet(), request)
    assert view_instance.get_queryset().query.order_by == ('-created_at',)


def test_field_age_group_is_auto_set_by_profile(api_rf, news_data, news_list_view, user_profile1_with_membership):
    expected_field_age_group = FieldOfStudyOfAgeGroup.objects.get_default_by_profile(user_profile1_with_membership)
    news_data.pop('field_age_group')
    request = api_rf.post(reverse('api:news-list'), data=news_data)
    MembershipFactory(profile=user_profile1_with_membership)
    force_authenticate(request, user_profile1_with_membership.user)
    response = news_list_view(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['field_age_group'] == expected_field_age_group.id
