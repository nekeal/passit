from datetime import timedelta

import factory
from django.utils import timezone

from .models import Event, EventCategoryChoices
from ..subject.factories import FieldOfStudyOfAgeGroupFactory


class EventFactory(factory.DjangoModelFactory):
    name = 'event'
    category = EventCategoryChoices.OTHER
    due_date = factory.LazyFunction(lambda: timezone.now() - timedelta(days=1))
    field_age_group = factory.SubFactory(FieldOfStudyOfAgeGroupFactory)

    class Meta:
        model = Event
