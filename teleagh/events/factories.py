from datetime import timedelta

import factory
from django.utils import timezone

from .models import Event, EventCategoryChoices


class EventFactory(factory.DjangoModelFactory):
    name = 'event'
    category = EventCategoryChoices.OTHER
    due_date = factory.LazyFunction(lambda: timezone.now() - timedelta(days=1))

    class Meta:
        model = Event
