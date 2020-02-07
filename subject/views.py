from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework import viewsets

from subject.models import FieldOfStudies, Subject, Resource
from subject.serializers import FieldOfStudiesBaseSerializer, SubjectBaseSerializer, ResourceBaseSerializer


class FieldOfStudiesViewSet(FlexFieldsModelViewSet):
    serializer_class = FieldOfStudiesBaseSerializer
    queryset = FieldOfStudies.objects.all()


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectBaseSerializer
    queryset = Subject.objects.all()


class ResourceViewSet(FlexFieldsModelViewSet):
    serializer_class = ResourceBaseSerializer
    queryset = Resource.objects.all()
    permit_list_expands = ('subject',)
