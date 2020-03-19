from typing import Dict, Tuple, Any

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.serializers import Serializer

from .models import Lecturer, LecturerOfSubjectOfAgeGroup


class LecturerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecturer
        fields = ('id', 'first_name', 'last_name', 'title', 'contact', 'consultations')


class LecturerOfSubjectOfAgeGroupSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = LecturerOfSubjectOfAgeGroup
        fields = ('id', 'lecturer',)
        expandable_fields: Dict[str, Tuple[Serializer, Dict[str, Any]]] = {
            'lecturer': (LecturerListSerializer, {}),
            'students_start_year': (serializers.IntegerField, {})
        }
