from typing import Dict, Any, Tuple

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.serializers import Serializer

from subject.models import FieldOfStudies, Subject, Resource


class FieldOfStudiesBaseSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = FieldOfStudies
        fields = ('id', 'name', 'slug')


class SubjectBaseSerializer(FlexFieldsModelSerializer):
    field_of_studies = serializers.CharField(source='field_of_studies.name')

    class Meta:
        model = Subject
        fields = ('id', 'name', 'semester', 'general_description', 'field_of_studies')
        expandable_fields: Dict[str, Tuple[Serializer, Dict[str, Any]]] = {
            'field_of_studies': (FieldOfStudiesBaseSerializer, {})
        }


class ResourceBaseSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Resource
        fields = ('id', 'name', 'image', 'url', 'description', 'subject', 'created_by', 'modified_by')
        expandable_fields: Dict[str, Tuple[Serializer, Dict[str, Any]]] = {
            'subject': (SubjectBaseSerializer, {'fields': ['id', 'name', 'semester', ]})
        }
