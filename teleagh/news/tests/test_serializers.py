from unittest import mock

from ..serializers import NewsSerializer


def test_serializer_have_correct_fields():
    assert set(NewsSerializer().fields) == {'id', 'title', 'content', 'subject_group', 'field_age_group', 'created_by',
                                            'modified_by', 'created_by_profile', 'modified_by_profile', 'created_at',
                                            'updated_at'}


def test_serializer_serializes_news(news):
    data = NewsSerializer(news)
    expected_data = {
        'id': news.id,
        'title': 'New timetable',
        'content': '',
        'subject_group': news.subject_group_id,
        'field_age_group': news.subject_group.field_age_group_id,
        'created_by': 'Anonymous',
        'modified_by': 'Anonymous',
        'created_at': data.data['created_at'],
        'updated_at': data.data['updated_at'],
    }

    assert data.data == expected_data


def test_serializer_can_create_news(subject_group):
    data = {
        'title': 'New timetable',
        'content': 'not blank',
        'subject_group': subject_group.id,
        'field_age_group': subject_group.field_age_group.id
    }
    news = NewsSerializer(data=data)
    news.is_valid(raise_exception=True)
    news.save()
    assert (news.instance.title, news.instance.subject_group_id) == (data['title'], data['subject_group'])


def test_content_cant_be_empty(subject_group):
    data = {
        'id': 1,
        'title': 'New timetable',
        'content': '',
        'subject_group': subject_group.id,
        'field_age_group': subject_group.field_age_group.id
    }
    serializer = NewsSerializer(data=data)
    serializer.is_valid()
    assert set(serializer.errors.keys()) == {'content',}


def test_news_owned_model_serializer(news_data, api_rf, user_profile1, user_profile2):
    request_user1 = mock.Mock()
    request_user1.user = user_profile1.user
    request_user2 = mock.Mock()
    request_user2.user = user_profile2.user
    serializer = NewsSerializer(data=news_data, context={'request': request_user1})
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    assert instance.created_by == user_profile1, "Creator is set on instace"
    assert instance.modified_by == user_profile1, "Modifier is set on instance"
    serializer = NewsSerializer(data=news_data, instance=instance, context={'request': request_user2})
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    assert instance.created_by == user_profile1, "Creator is unchanged on instance"
    assert instance.modified_by == user_profile2, "Modifier is changed on instance"
