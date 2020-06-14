from django.db.models import F
from rest_flex_fields import is_expanded
from rest_framework import viewsets

from teleagh.events.filters import EventFilterSet
from teleagh.events.models import Event
from teleagh.events.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.select_related('created_by__user', 'modified_by__user')
    serializer_class = EventSerializer
    filterset_class = EventFilterSet

    def get_queryset(self):
        queryset = Event.objects.filter_by_user_profile_default_field_age_group(self.request.user.profile)\
            .select_related('created_by__user', 'modified_by__user')
        if is_expanded(self.request, 'subject') or True:
            queryset = queryset.annotate(subject=F('subject_group__subject__name'))
        if is_expanded(self.request, 'field_age_group'):
            queryset = queryset.select_related('field_age_group')
        if is_expanded(self.request, 'subject_group'):
            queryset = queryset.select_related('subject_group')
        if is_expanded(self.request, 'subject'):
            queryset = queryset.select_related('subject_group__subject')
        return queryset.order_by('due_date')
