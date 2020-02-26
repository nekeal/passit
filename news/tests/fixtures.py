import pytest

from news.factories import NewsFactory


@pytest.fixture
def news(db, subject_group):
    return NewsFactory(title="New timetable", subject_group=subject_group)


@pytest.fixture
def news_data(subject_group):
    return {
        'title': 'New timetable',
        'content': 'not blank',
        'field_age_group': subject_group.field_age_group.id,
        'subject_group': subject_group.id,
    }
