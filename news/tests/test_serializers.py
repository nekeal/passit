from news.serializers import NewsSerializer


def test_serializer_have_correct_fields():
    assert set(NewsSerializer().fields) == {'id', 'title', 'content', 'subject_group', 'field_age_group'}


def test_serializer_serializes_news(news):
    data = NewsSerializer(news)
    expected_data = {
        'id': news.id,
        'title': 'New timetable',
        'content': '',
        'subject_group': news.subject_group_id,
        'field_age_group': news.subject_group.field_age_group_id
    }
    assert data.data == expected_data


def test_serializer_can_create_news(news_data):
    news = NewsSerializer(data=news_data)
    news.is_valid(raise_exception=True)
    news.save()
    assert (news.instance.title, news.instance.subject_group_id) == (news_data['title'], news_data['subject_group'])


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
