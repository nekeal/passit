from news.serializers import NewsBaseSerializer


def test_serializer_have_correct_fields():
    assert set(NewsBaseSerializer().fields) == {'id', 'title', 'content', 'subject_group'}


def test_serializer_serializes_news(news):
    data = NewsBaseSerializer(news)
    expected_data = {
        'id': news.id,
        'title': 'New timetable',
        'content': '',
        'subject_group': news.subject_group_id
    }
    assert data.data == expected_data


def test_serializer_can_create_news(subject_group):
    data = {
        'id': 1,
        'title': 'New timetable',
        'content': 'not blank',
        'subject_group': subject_group.id
    }
    news = NewsBaseSerializer(data=data)
    news.is_valid(raise_exception=True)
    news.save()
    assert (news.instance.title, news.instance.subject_group_id) == (data['title'], data['subject_group'])


def test_content_cant_be_empty(subject_group):
    data = {
        'id': 1,
        'title': 'New timetable',
        'content': '',
        'subject_group': subject_group.id
    }
    serializer = NewsBaseSerializer(data=data)
    serializer.is_valid()
    assert set(serializer.errors.keys()) == {'content',}
