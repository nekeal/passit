import django_filters

from teleagh.subject.models import Subject


class SubjectFilterSet(django_filters.FilterSet):

    class Meta:
        model = Subject
        fields = ('semester',)
