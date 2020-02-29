from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from .models import CustomUser, Membership, UserProfile


class MembershipSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Membership
        fields = ('id', 'profile', 'field_age_group', 'type')


class ProfileSerializer(FlexFieldsModelSerializer):
    memberships = MembershipSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('memberships',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'profile')
