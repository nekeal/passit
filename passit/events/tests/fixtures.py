from datetime import timedelta

import pytest
from django.utils import timezone

from passit.events.factories import EventFactory
from passit.events.models import EventCategoryChoices


@pytest.fixture
def event(field_age_group):
    return EventFactory(name='event',
                        category=EventCategoryChoices.OTHER,
                        due_date=timezone.now() - timedelta(days=1),
                        field_age_group=field_age_group)


@pytest.fixture
def event_data(field_age_group):
    return {
        "name": "event",
        "description": "",
        "category": EventCategoryChoices.OTHER,
        "due_date": str(timezone.now() - timedelta(days=1)),
        "field_age_group": field_age_group.id,
    }


@pytest.fixture
def event_with_subject_group_data(field_age_group, subject_group):
    return {
        "name": "event",
        "description": "",
        "category": EventCategoryChoices.OTHER,
        "due_date": str(timezone.now() - timedelta(days=1)),
        "field_age_group": field_age_group.id,
        "subject_group": subject_group.id,
    }
