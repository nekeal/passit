from typing import Any, Dict, Tuple

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.serializers import Serializer

from .models import Lecturer, LecturerOfSubjectOfAgeGroup


class LecturerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ("id", "first_name", "last_name", "title", "contact", "consultations")


class LecturerSyllabusImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ("first_name", "last_name", "title")

    def create(self, validated_data):
        lecturer, created = Lecturer.objects.get_or_create(**validated_data)
        return lecturer


class LecturerOfSubjectOfAgeGroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = LecturerOfSubjectOfAgeGroup
        fields = (
            "id",
            "lecturer",
        )
        expandable_fields: Dict[str, Tuple[Serializer, Dict[str, Any]]] = {
            "lecturer": (LecturerBaseSerializer, {}),
            "students_start_year": (serializers.IntegerField, {}),
        }
