from rest_flex_fields import FlexFieldsModelSerializer

from news.models import News


class NewsSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'subject_group', 'field_age_group')
