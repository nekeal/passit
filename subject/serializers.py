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
    field_of_studies = serializers.CharField(source='field_of_studies.name', read_only=True)
    field_of_studies_pk = serializers.PrimaryKeyRelatedField(write_only=True, queryset=FieldOfStudies.objects.all())

    class Meta:
        model = Subject
        fields = ('id', 'name', 'semester', 'general_description', 'field_of_studies', 'field_of_studies_pk')

    def create(self, validated_data):
        validated_data["field_of_studies"] = validated_data.pop("field_of_studies_pk")
        print(validated_data)
        return super().create(validated_data)


class ResourceListSerializer(serializers.ModelSerializer):
    is_image = serializers.SerializerMethodField(source='image', read_only=True)
    is_url = serializers.SerializerMethodField(source='url', read_only=True)

    def get_is_image(self, instance):
        return True if instance.image else False

    def get_is_url(self, instance):
        return True if instance.url else False

    class Meta:
        model = Resource
        fields = ('id', 'name', 'is_url', 'is_image', 'url')


class ResourceDetailSerializer(serializers.ModelSerializer):
    subject = SubjectListSerializer(read_only=True)
    subject_pk = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Subject.objects.all())

    class Meta:
        model = Resource
        fields = ('id', 'name', 'image', 'url', 'description', 'subject', 'subject_pk', 'created_by', 'modified_by')

    def create(self, validated_data):
        validated_data['subject'] = validated_data.pop('subject_pk')
        return super(ResourceDetailSerializer, self).create(validated_data)
