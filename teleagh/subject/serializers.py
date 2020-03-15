from typing import Dict, Any, Tuple

from django.db.models import QuerySet
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.serializers import Serializer

from ..common.serializers import OwnedModelSerializerMixin
from ..lecturers.models import LecturerOfSubjectOfAgeGroup
from ..lecturers.serializers import LecturerOfSubjectOfAgeGroupSerializer
from ..subject.models import FieldOfStudy, Subject, Resource, FieldOfStudyOfAgeGroup


class FieldAgeGroupRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self) -> 'QuerySet[FieldOfStudyOfAgeGroup]':
        request = self.context.get('request')
        profile = request and request.user and request.user.profile
        if not profile:
            return FieldOfStudyOfAgeGroup.objects.all()
        return FieldOfStudyOfAgeGroup.objects.filter_by_profile(profile)


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

    def get_lecturers(self, instance: Subject):
        lecturers_of_age_group = LecturerOfSubjectOfAgeGroup.objects.filter(subject_group__subject=instance.id).\
            annotate_students_start_year()
        serializer = LecturerOfSubjectOfAgeGroupSerializer(lecturers_of_age_group, many=True,
                                                           expand=['lecturer', 'students_start_year'])
        return serializer.data

    class Meta:
        model = Subject
        fields = ('id', 'name', 'semester', 'general_description', 'field_of_study')
        expandable_fields: Dict[str, Tuple[Serializer, Dict[str, Any]]] = {
            'field_of_study': (FieldOfStudyBaseSerializer, {}),
            'lecturers': (serializers.SerializerMethodField, {})
        }


class ResourceBaseSerializer(OwnedModelSerializerMixin, FlexFieldsModelSerializer):

    class Meta:
        model = Resource
        fields = ('id', 'name', 'image', 'url', 'description', 'subject', 'category', 'created_by_profile',
                  'modified_by_profile', 'created_by', 'modified_by')
        expandable_fields: Dict[str, Tuple[Serializer, Dict[str, Any]]] = {
            'subject': (SubjectBaseSerializer, {'fields': ['id', 'name', 'semester', ]})
        }
