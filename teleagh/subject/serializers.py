from typing import Dict, Any, Tuple

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.serializers import Serializer

from ..subject.models import FieldOfStudy, Subject, Resource, FieldOfStudyOfAgeGroup


class FieldOfStudyBaseSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = FieldOfStudy
        fields = ('id', 'name', 'slug')


class FieldOfStudyOfAgeGroupSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = FieldOfStudyOfAgeGroup
        fields = ('id', 'field_of_study', 'students_start_year', )
        expandable_fields: Dict[str, Tuple[Serializer, Dict[str, Any]]] = {
            'field_of_study': (FieldOfStudyBaseSerializer, {})
        }


class SubjectBaseSerializer(FlexFieldsModelSerializer):
    field_of_study = serializers.CharField(source='field_of_study.name')

    class Meta:
        model = Subject
        fields = ('id', 'name', 'semester', 'general_description', 'field_of_study')
        expandable_fields: Dict[str, Tuple[Serializer, Dict[str, Any]]] = {
            'field_of_study': (FieldOfStudyBaseSerializer, {})
        }


class ResourceBaseSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Resource
        fields = ('id', 'name', 'image', 'url', 'description', 'subject', 'category', 'created_by', 'modified_by')
        expandable_fields: Dict[str, Tuple[Serializer, Dict[str, Any]]] = {
            'subject': (SubjectBaseSerializer, {'fields': ['id', 'name', 'semester', ]})
        }
