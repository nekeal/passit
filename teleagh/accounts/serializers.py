from typing import Dict, Tuple, Any

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from .models import CustomUser, Membership, UserProfile
from ..subject.serializers import FieldOfStudyOfAgeGroupSerializer, FieldAgeGroupRelatedField


class MembershipSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Membership
        fields = ('id', 'profile', 'field_age_group', 'type', 'is_default')


class ProfileSerializer(FlexFieldsModelSerializer):  # TODO optimize queryset

    class Meta:
        model = UserProfile
        fields = ('memberships', 'field_age_groups')
        expandable_fields: Dict[str, Tuple[serializers.Serializer, Dict[str, Any]]] = {
            'field_age_groups': (FieldOfStudyOfAgeGroupSerializer, {'many': True}),
            'memberships': (MembershipSerializer, {'many': True})
        }


class CustomUserSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'profile', 'first_name', 'last_name')
        expandable_fields: Dict[str, Tuple[serializers.Serializer, Dict[str, Any]]] = {
            'profile': (ProfileSerializer, {})
        }


class DefaultFieldOfAgeGroupSerializer(serializers.Serializer):
    field_age_group = FieldAgeGroupRelatedField(write_only=True)

    def update(self, instance: 'UserProfile', validated_data):
        new_default = instance.set_default_field_age_group(validated_data['field_age_group'])
        return new_default
