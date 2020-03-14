from rest_flex_fields import FlexFieldsModelViewSet

from .filters import SubjectFilterSet, ResourceFilterSet
from ..subject.models import FieldOfStudy, Subject, Resource
from ..subject.serializers import FieldOfStudyBaseSerializer, SubjectBaseSerializer, ResourceBaseSerializer


class FieldOfStudiesViewSet(FlexFieldsModelViewSet):
    serializer_class = FieldOfStudyBaseSerializer
    queryset = FieldOfStudy.objects.all()


class SubjectViewSet(FlexFieldsModelViewSet):
    serializer_class = SubjectBaseSerializer
    queryset = Subject.objects.select_related('field_of_study')
    filterset_class = SubjectFilterSet


class ResourceViewSet(FlexFieldsModelViewSet):
    serializer_class = ResourceBaseSerializer
    queryset = Resource.objects.all()
    filterset_class = ResourceFilterSet
    permit_list_expands = ('subject',)
