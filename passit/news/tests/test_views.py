from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate

from ..factories import NewsFactory
from ..managers import NewsManager
from ..models import News
from ..views import NewsViewSet
from ...accounts.factories import MembershipFactory
from ...common.utils import setup_view
from ...subject.models import FieldOfStudyOfAgeGroup


@pytest.fixture
def news_list_view():
    return NewsViewSet.as_view({'get': 'list', 'post': 'create'})


@pytest.fixture
def news_detail_view():
    return NewsViewSet.as_view({'get': 'retrieve', 'post': 'create', 'delete': 'destroy', 'put': 'update'})


# --- NewsViewSet ---

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


def test_field_age_group_is_auto_set_by_profile(api_rf, news_data, news_list_view, student1):
    expected_field_age_group = FieldOfStudyOfAgeGroup.objects.get_default_by_profile(student1)
    news_data.pop('field_age_group')
    request = api_rf.post(reverse('api:news-list'), data=news_data)
    MembershipFactory(profile=student1)
    force_authenticate(request, student1.user)
    response = news_list_view(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['field_age_group'] == expected_field_age_group.id


def test_is_news_owner_flag_is_in_response(api_rf, news_list_view, student1,
                                           student2, field_age_group):
    request = api_rf.get(reverse('api:news-list'), data={'expand': 'is_news_owner'})
    force_authenticate(request, student1.user)
    owned_by_user1 = NewsFactory(created_by=student1,
                                 field_age_group=field_age_group)
    owned_by_user2 = NewsFactory(created_by=student2,
                                 field_age_group=field_age_group)
    response = news_list_view(request)
    news = response.data
    assert news[0]['is_owner'] if news[0]['id'] == owned_by_user1.id else not news[0]['is_owner']
    assert not news[1]['is_owner'] if news[1]['id'] == owned_by_user2.id else news[1]['is_owner']


def test_is_owner_is_returned_when_creating_news(api_rf, news_list_view, news_data, student1):
    request = api_rf.post(reverse('api:news-list'), data=news_data)
    force_authenticate(request, student1.user)
    response = news_list_view(request)
    assert response.data['is_owner']


def test_every_authenticated_user_can_create_news(api_rf, news_list_view, news_data, student1):
    request = api_rf.post(reverse('api:news-list'), data=news_data)
    force_authenticate(request, student1.user)
    response = news_list_view(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert News.objects.count() == 1


def test_owner_can_update_news(api_rf, news_detail_view, news_data, subject_group, student1):
    news = NewsFactory(subject_group=subject_group, created_by=student1)
    new_title = "New Title"
    news_data['title'] = new_title
    request = api_rf.put(reverse('api:news-detail', args=(news.id,)), data=news_data)
    force_authenticate(request, student1.user)
    response = news_detail_view(request, pk=news.id)
    news.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert news.title == new_title


def test_privileged_can_update_news(api_rf, news_detail_view, news_data, subject_group,
                                    student1, representative_profile):
    news = NewsFactory(subject_group=subject_group, created_by=student1)
    new_title = "New Title"
    news_data['title'] = new_title
    request = api_rf.put(reverse('api:news-detail', args=(news.id,)), data=news_data)
    force_authenticate(request, representative_profile.user)
    response = news_detail_view(request, pk=news.id)
    news.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert news.title == new_title


def test_user_cant_update_not_his_news(api_rf, news_detail_view, news_data, subject_group, student1, student2):
    news = NewsFactory(subject_group=subject_group, created_by=student1)
    new_title = "New Title"
    news_data['title'] = new_title
    request = api_rf.put(reverse('api:news-detail', args=(news.id,)), data=news_data)
    force_authenticate(request, student2.user)
    response = news_detail_view(request, pk=news.id)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_owner_can_delete_news(api_rf, news_detail_view, news_data, subject_group, student1):
    news = NewsFactory(subject_group=subject_group, created_by=student1)
    request = api_rf.delete(reverse('api:news-detail', args=(news.id,)))
    force_authenticate(request, student1.user)
    response = news_detail_view(request, pk=news.id)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert News.objects.count() == 0


def test_user_cant_delete_not_his_news(api_rf, news_detail_view, news_data, subject_group, student1, student2):
    news = NewsFactory(subject_group=subject_group, created_by=student1)
    request = api_rf.delete(reverse('api:news-detail', args=(news.id,)))
    force_authenticate(request, student2.user)
    response = news_detail_view(request, pk=news.id)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert News.objects.count() == 1


def test_privileged_can_delete_news(api_rf, news_detail_view, news_data, subject_group, student1,
                                    representative_profile):
    news = NewsFactory(subject_group=subject_group, created_by=student1)
    request = api_rf.delete(reverse('api:news-detail', args=(news.id,)))
    force_authenticate(request, representative_profile.user)
    response = news_detail_view(request, pk=news.id)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert News.objects.count() == 0
