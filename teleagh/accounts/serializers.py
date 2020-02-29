from typing import Dict, Tuple, Any

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.serializers import Serializer

from .models import CustomUser, Membership, UserProfile
from ..subject.serializers import FieldOfStudyOfAgeGroupSerializer


class MembershipSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Membership
        fields = ('id', 'profile', 'field_age_group', 'type')


class ProfileSerializer(FlexFieldsModelSerializer):  # TODO optimize queryset

    class Meta:
        model = UserProfile
        fields = ('memberships', 'field_age_groups')
        expandable_fields: Dict[str, Tuple[Serializer, Dict[str, Any]]] = {
            'field_age_groups': (FieldOfStudyOfAgeGroupSerializer, {'many': True}),
            'memberships': (MembershipSerializer, {'many': True})
        }


class CustomUserSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'profile')
        expandable_fields: Dict[str, Tuple[Serializer, Dict[str, Any]]] = {
            'profile': (ProfileSerializer, {})
        }
