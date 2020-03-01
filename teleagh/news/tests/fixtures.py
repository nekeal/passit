import pytest

from teleagh.news.factories import NewsFactory


@pytest.fixture
def news(db, subject_group):
    return NewsFactory(title="New timetable", subject_group=subject_group)
