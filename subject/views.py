from rest_framework import viewsets
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin

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


class ResourceViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = ResourceListSerializer
    queryset = Resource.objects.all()
    # extensions_expand = {"subject"}
    # extensions_only = {'name', 'url'}
    def get_serializer_class(self):
        if self.action != 'list':
            print("DETAIL")
            return ResourceDetailSerializer
        return super(ResourceViewSet, self).get_serializer_class()
