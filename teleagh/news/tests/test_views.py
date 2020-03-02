from unittest import mock

import pytest
from django.urls import reverse
from rest_framework.test import force_authenticate

from ..managers import NewsManager
from ..models import News
from ..views import NewsViewSet


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
