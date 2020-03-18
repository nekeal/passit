from rest_flex_fields import FlexFieldsModelSerializer

from .models import News
from ..common.serializers import OwnedModelSerializerMixin
from ..subject.serializers import FieldAgeGroupRelatedField, FieldAgeGroupDefault


class NewsSerializer(OwnedModelSerializerMixin, FlexFieldsModelSerializer):
    field_age_group = FieldAgeGroupRelatedField(default=FieldAgeGroupDefault())

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'subject_group', 'field_age_group', 'created_by_profile',
                  'modified_by_profile', 'created_by', 'modified_by', 'created_at', 'updated_at')
