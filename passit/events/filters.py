import django_filters

from .models import Event


class EventFilterSet(django_filters.FilterSet):
    due_date = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Event
        fields = ('due_date',)
