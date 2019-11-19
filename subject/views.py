from rest_framework import viewsets

from subject.models import FieldOfStudies, Subject, Resource
from subject.serializers import FieldOfStudiesSerializer, SubjectListSerializer, SubjectDetailSerializer, \
    ResourceListSerializer, ResourceDetailSerializer


class FieldOfStudiesViewSet(viewsets.ModelViewSet):
    serializer_class = FieldOfStudiesSerializer
    queryset = FieldOfStudies.objects.all()
    model = FieldOfStudies


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectListSerializer
    queryset = Subject.objects.all()

    def get_serializer_class(self):
        if self.action != 'list':
            return SubjectDetailSerializer
        return super(SubjectViewSet, self).get_serializer_class()


class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceListSerializer
    queryset = Resource.objects.all()

    def get_serializer_class(self):
        if self.action != 'list':
            return ResourceDetailSerializer
        return super(ResourceViewSet, self).get_serializer_class()
