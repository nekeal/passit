from rest_flex_fields import FlexFieldsModelViewSet, is_expanded

from .filters import SubjectFilterSet, ResourceFilterSet
from ..subject.models import FieldOfStudy, Subject, Resource, SubjectOfAgeGroup
from ..subject.serializers import FieldOfStudyBaseSerializer, SubjectBaseSerializer, ResourceBaseSerializer, \
    SubjectOfAgeGroupSerializer


class FieldOfStudiesViewSet(FlexFieldsModelViewSet):
    serializer_class = FieldOfStudyBaseSerializer
    queryset = FieldOfStudy.objects.all()


class SubjectViewSet(FlexFieldsModelViewSet):
    serializer_class = SubjectBaseSerializer
    queryset = Subject.objects.select_related('field_of_study')
    filterset_class = SubjectFilterSet
    permit_list_expands = ['field_of_study']


class SubjectOfAgeGroupViewSet(FlexFieldsModelViewSet):
    serializer_class = SubjectOfAgeGroupSerializer
    permit_list_expands = ['field_age_group', 'subject_name']

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
    permit_list_expands = ('subject',)
