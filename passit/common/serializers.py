from typing import Optional

from rest_framework import serializers
from rest_framework.fields import Field

from passit.accounts.models import UserProfile


class CurrentUserProfileDefault:
    requires_context = True

    def __call__(self, serializer_field: Field) -> "Optional[UserProfile]":
        request = serializer_field.context.get("request")
        if request and request.user and request.user.profile:
            return request.user.profile
        return None

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class OwnedModelSerializerMixin(metaclass=serializers.SerializerMetaclass):
    created_by = serializers.SerializerMethodField(read_only=True)
    modified_by = serializers.SerializerMethodField(read_only=True)
    created_by_profile = serializers.HiddenField(
        source="created_by",
        default=serializers.CreateOnlyDefault(CurrentUserProfileDefault()),
    )
    modified_by_profile = serializers.HiddenField(
        source="modified_by", default=CurrentUserProfileDefault()
    )

    @staticmethod
    def get_created_by(instance):
        if instance.created_by:
            return instance.created_by.get_name()
        return "Anonymous"

    @staticmethod
    def get_modified_by(instance):
        if instance.modified_by:
            return instance.modified_by.get_name()
        return "Anonymous"
