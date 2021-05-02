from rest_flex_fields import FlexFieldsModelViewSet, is_expanded
from rest_framework.permissions import IsAuthenticated

from .filters import ResourceFilterSet, SubjectFilterSet, SubjectOfAgeGroupFilterSet
from ..common.permissions import IsPrivilegedOrOwnerOrReadOnly
from ..subject.models import FieldOfStudy, Resource, Subject, SubjectOfAgeGroup
from ..subject.serializers import (
    FieldOfStudyBaseSerializer,
    ResourceBaseSerializer,
    SubjectBaseSerializer,
    SubjectOfAgeGroupSerializer,
)


class FieldOfStudiesViewSet(FlexFieldsModelViewSet):
    serializer_class = FieldOfStudyBaseSerializer
    queryset = FieldOfStudy.objects.all()
    permission_classes = [IsPrivilegedOrOwnerOrReadOnly]

    def get_queryset(self):
        return FieldOfStudy.objects.filter_by_profile(self.request.user.profile)


class SubjectViewSet(FlexFieldsModelViewSet):
    serializer_class = SubjectBaseSerializer
    queryset = Subject.objects.select_related('field_of_study')
    filterset_class = SubjectFilterSet
    permit_list_expands = ['field_of_study']

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter_by_profile(self.request.user.profile)


class SubjectOfAgeGroupViewSet(FlexFieldsModelViewSet):
    serializer_class = SubjectOfAgeGroupSerializer
    permit_list_expands = ['field_age_group', 'subject_name']
    filterset_class = SubjectOfAgeGroupFilterSet

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = SubjectOfAgeGroup.objects.filter_by_profile(profile)
        if is_expanded(self.request, 'field_age_group'):
            queryset = queryset.select_related('field_age_group')
        if is_expanded(self.request, 'subject_name'):
            queryset = queryset.add_subject_name()
        return queryset


class ResourceViewSet(FlexFieldsModelViewSet):
    serializer_class = ResourceBaseSerializer
    queryset = Resource.objects.all()
    filterset_class = ResourceFilterSet
    permission_classes = [
        IsAuthenticated,
    ]
    permit_list_expands = ('subject',)

    def get_queryset(self):
        qs = Resource.objects.filter_by_profile(self.request.user.profile)
        if is_expanded(self.request, "subject"):
            qs = qs.select_related("subject")
        return qs
