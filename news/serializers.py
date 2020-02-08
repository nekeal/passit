from rest_flex_fields import FlexFieldsModelSerializer

from news.models import News


class NewsBaseSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'subject_group')
