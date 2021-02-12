import pytest

from passit.news.factories import NewsFactory
from passit.news.models import News


@pytest.fixture
def news(db, subject_group) -> News:
    return NewsFactory(title="New timetable", subject_group=subject_group)


@pytest.fixture
def news_data(subject_group):
    return {
        'title': 'New timetable',
        'content': 'content',
        'subject_group': subject_group.id,
        'field_age_group': subject_group.field_age_group_id
    }
