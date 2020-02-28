import django_filters

from .models import News


class NewsFilterSet(django_filters.FilterSet):

    class Meta:
        model = News
        fields = ('id', 'subject_group', 'field_age_group')
