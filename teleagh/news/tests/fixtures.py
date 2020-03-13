import pytest

from teleagh.news.factories import NewsFactory
from teleagh.news.models import News


@pytest.fixture
def news(db, subject_group) -> News:
    return NewsFactory(title="New timetable", subject_group=subject_group)


@pytest.fixture
def news_data(news, subject_group):
    return {
        'title': 'New timetable',
        'content': 'content',
        'subject_group': news.subject_group_id,
        'field_age_group': news.subject_group.field_age_group_id
    }
