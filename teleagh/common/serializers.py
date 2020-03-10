from typing import Optional

from rest_framework import serializers

from teleagh.accounts.models import UserProfile


class CurrentUserProfileDefault:

    def __init__(self) -> None:
        self.profile: Optional[UserProfile] = None

    def set_context(self, serializer_field) -> None:
        request = serializer_field.context.get('request')
        if request and request.user and request.user.profile:
            self.profile = serializer_field.context['request'].user.profile

    def __call__(self, *args, **kwargs) -> 'Optional[UserProfile]':
        return self.profile

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class OwnedModelSerializerMixin(metaclass=serializers.SerializerMetaclass):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    modified_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by_profile = serializers.HiddenField(source='created_by', default=serializers.CreateOnlyDefault(CurrentUserProfileDefault()))
    modified_by_profile = serializers.HiddenField(source='modified_by', default=CurrentUserProfileDefault())
