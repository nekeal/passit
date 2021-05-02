from unittest import mock

from ..serializers import NewsSerializer


# --- NewsSerializer ---


def test_serializer_have_correct_fields():
    assert set(NewsSerializer().fields) == {
        'id',
        'title',
        'content',
        'subject_group',
        'field_age_group',
        'attachment',
        'created_by',
        'modified_by',
        'created_by_profile',
        'modified_by_profile',
        'created_at',
        'updated_at',
        'is_owner',
    }


def test_serializer_serializes_news(news, user_profile1, user_profile2):
    request = mock.Mock()
    request.user = user_profile1.user
    news.created_by = user_profile1
    news.modified_by = user_profile2
    data = NewsSerializer(news, context={'request': request})
    expected_data = {
        'id': news.id,
        'title': 'New timetable',
        'content': '',
        'subject_group': news.subject_group_id,
        'field_age_group': news.subject_group.field_age_group_id,
        'created_by': user_profile1.get_name(),
        'modified_by': user_profile2.get_name(),
        'created_at': data.data['created_at'],
        'updated_at': data.data['updated_at'],
        'attachment': None,
        'is_owner': True,
    }

    assert data.data == expected_data


def test_serializer_can_create_news(student1, subject_group):
    request = mock.Mock()
    request.user = student1.user
    data = {
        'title': 'New timetable',
        'content': 'not blank',
        'subject_group': subject_group.id,
        'field_age_group': subject_group.field_age_group.id,
    }
    news = NewsSerializer(data=data, context={'request': request})
    news.is_valid(raise_exception=True)
    news.save()
    assert (
        news.instance.title,
        news.instance.subject_group_id,
        news.instance.field_age_group_id,
    ) == (data['title'], data['subject_group'], subject_group.field_age_group_id)


def test_content_cant_be_empty(subject_group):
    data = {
        'id': 1,
        'title': 'New timetable',
        'content': '',
        'subject_group': subject_group.id,
        'field_age_group': subject_group.field_age_group.id,
    }
    serializer = NewsSerializer(data=data)
    serializer.is_valid()
    assert set(serializer.errors.keys()) == {
        'content',
    }


def test_news_owned_model_serializer(news_data, api_rf, student1, student2):
    request_user1 = mock.Mock()
    request_user1.user = student1.user
    request_user2 = mock.Mock()
    request_user2.user = student2.user
    serializer = NewsSerializer(data=news_data, context={'request': request_user1})
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    assert instance.created_by == student1, "Creator is set on instace"
    assert instance.modified_by == student1, "Modifier is set on instance"
    serializer = NewsSerializer(
        data=news_data, instance=instance, context={'request': request_user2}
    )
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    assert instance.created_by == student1, "Creator is unchanged on instance"
    assert instance.modified_by == student2, "Modifier is changed on instance"
