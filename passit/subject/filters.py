import django_filters

from .models import Resource, Subject, SubjectOfAgeGroup


class SubjectFilterSet(django_filters.FilterSet):
    class Meta:
        model = Subject
        fields = ("semester", "field_of_study")


class SubjectOfAgeGroupFilterSet(django_filters.FilterSet):
    class Meta:
        model = SubjectOfAgeGroup
        fields = ("field_age_group",)


class ResourceFilterSet(django_filters.FilterSet):
    class Meta:
        model = Resource
        fields = ("subject", "category")
