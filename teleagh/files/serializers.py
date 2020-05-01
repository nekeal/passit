from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import File
from ..common.serializers import OwnedModelSerializerMixin


class FileSerializer(OwnedModelSerializerMixin, serializers.ModelSerializer):
    thumbnails = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id', 'name', 'other', 'image', 'thumbnails')

    def get_thumbnails(self, obj: File):
        request = self.context.get('request')
        if obj.image:
            thumbnails = obj.get_thumbnails()
            return {name: self.build_url(thumbnail, request) for name, thumbnail in thumbnails.items()}

    @staticmethod
    def build_url(thumbnail, request=None) -> str:
        if request:
            return request.build_absolute_uri(thumbnail.url)
        return thumbnail.url

    def validate(self, attrs):
        if all((attrs.get('other'), attrs.get('image'))):
            raise ValidationError(_('Only one of image and other should be chosen'))
        elif not any((attrs.get('other'), attrs.get('image'))):
            raise ValidationError(_('One of image and other should be chosen'))
        return attrs
