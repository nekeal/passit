from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from subject.models import FieldOfStudies, Subject, Resource
from subject.serializers import FieldOfStudiesSerializer, SubjectListSerializer, SubjectDetailSerializer, \
    ResourceListSerializer, ResourceDetailSerializer


class FieldOfStudiesViewSet(viewsets.ModelViewSet):
    serializer_class = FieldOfStudiesSerializer
    queryset = FieldOfStudies.objects.all()
    model = FieldOfStudies


    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        field = self.get_object()
        subjects = Subject.objects.filter(field_of_studies=field)
        serializer = SubjectListSerializer(subjects, many=True)
        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectListSerializer
    queryset = Subject.objects.all()

    def get_serializer_class(self):
        if self.action != 'list':
            return SubjectDetailSerializer
        return super(SubjectViewSet, self).get_serializer_class()

    @action(detail=True, methods=['get'])
    def resources(self, request, pk=None):
        subject = self.get_object()
        resources = Resource.objects.filter(subject=subject)
        serializer = ResourceListSerializer(resources, many=True)
        return Response(serializer.data)


class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceListSerializer
    queryset = Resource.objects.all()

    def get_serializer_class(self):
        if self.action != 'list':
            return ResourceDetailSerializer
        return super(ResourceViewSet, self).get_serializer_class()
