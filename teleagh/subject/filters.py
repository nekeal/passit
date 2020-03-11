import django_filters

from .models import Subject, Resource


class SubjectFilterSet(django_filters.FilterSet):

    class Meta:
        model = Subject
        fields = ('semester',)


class ResourceFilterSet(django_filters.FilterSet):

    class Meta:
        model = Resource
        fields = ('subject',)
