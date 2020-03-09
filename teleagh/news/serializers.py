from rest_flex_fields import FlexFieldsModelSerializer

from .models import News
from ..common.serializers import OwnedModelSerializerMixin


class NewsSerializer(OwnedModelSerializerMixin, FlexFieldsModelSerializer):

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'subject_group', 'field_age_group', 'created_by', 'modified_by',
                  'created_at', 'updated_at')
