from typing import Any, Dict, Tuple

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..subject.serializers import (
    FieldAgeGroupRelatedField,
    FieldOfStudyOfAgeGroupSerializer,
)
from .models import CustomUser, Membership, UserProfile


class MembershipSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Membership
        fields = ("id", "profile", "field_age_group", "type", "is_default")


class ProfileSerializer(FlexFieldsModelSerializer):  # TODO optimize queryset
    class Meta:
        model = UserProfile
        fields = ("memberships", "field_age_groups")
        expandable_fields: Dict[str, Tuple[serializers.Serializer, Dict[str, Any]]] = {
            "field_age_groups": (FieldOfStudyOfAgeGroupSerializer, {"many": True}),
            "memberships": (MembershipSerializer, {"many": True}),
        }


class CustomUserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "profile", "first_name", "last_name")
        expandable_fields: Dict[str, Tuple[serializers.Serializer, Dict[str, Any]]] = {
            "profile": (ProfileSerializer, {})
        }


class DefaultFieldOfAgeGroupSerializer(serializers.Serializer):
    field_age_group = FieldAgeGroupRelatedField(write_only=True)

    def update(self, instance: "UserProfile", validated_data):
        new_default = instance.set_default_field_age_group(
            validated_data["field_age_group"]
        )
        return new_default


class StudentsImportSerializer(serializers.Serializer):
    """
    Serializer is used by StudentImportService.
    Necessary kwargs are passed to .save() method.
    """

    username = serializers.CharField(max_length=150)
    password = serializers.CharField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    class Meta:
        model = CustomUser

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise ValidationError("User with this username already exists")
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_student(**validated_data)
