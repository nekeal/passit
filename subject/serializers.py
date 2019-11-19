from rest_framework import serializers

from subject.models import FieldOfStudies, Subject, Resource


class FieldOfStudiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldOfStudies
        fields = ('id', 'name', 'slug')


class SubjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ('id', 'name', 'semester',)


class SubjectDetailSerializer(serializers.ModelSerializer):
    field_of_studies = serializers.CharField(source='field_of_studies.name')

    class Meta:
        model = Subject
        fields = ('id', 'name', 'semester', 'general_description', 'field_of_studies')


class ResourceListSerializer(serializers.ModelSerializer):
    is_image = serializers.SerializerMethodField(source='image', read_only=True)
    is_url = serializers.SerializerMethodField(source='url', read_only=True)

    def get_is_image(self, instance):
        return True if instance.image else False

    def get_is_url(self, instance):
        return True if instance.url else False

    class Meta:
        model = Resource
        fields = ('id', 'name', 'is_url', 'is_image')


class ResourceDetailSerializer(serializers.ModelSerializer):
    subject = SubjectListSerializer(read_only=True)

    class Meta:
        model = Resource
        fields = ('id', 'name', 'image', 'url', 'description', 'subject', 'created_by', 'modified_by')
