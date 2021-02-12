from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from .models import News
from ..common.serializers import OwnedModelSerializerMixin
from ..subject.serializers import FieldAgeGroupRelatedField, FieldAgeGroupDefault


class NewsSerializer(OwnedModelSerializerMixin, FlexFieldsModelSerializer):
    field_age_group = FieldAgeGroupRelatedField(default=FieldAgeGroupDefault())
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, instance):
        if hasattr(instance, 'is_news_owner'):
            return instance.is_news_owner
        return instance.is_owner(self.context['request'].user.profile)

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'subject_group', 'field_age_group', 'attachment', 'created_by_profile',
                  'modified_by_profile', 'is_owner', 'created_by', 'modified_by', 'created_at', 'updated_at')
