from unittest import mock

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from teleagh.files.serializers import FileSerializer


class TestFileSerializer:

    def test_image_or_other_should_be_set(self, api_rf, file_other_data):
        file_other_data.pop('other')
        serializer = FileSerializer(data=file_other_data)
        serializer.is_valid()
        assert 'One of' in serializer.errors['non_field_errors'][0]

    @pytest.mark.django_db
    def test_image_or_other_cant_be_set_together(self, api_rf, file_other_data, image_file):
        file_other_data['image'] = SimpleUploadedFile('a.jpg', content=image_file.read(),
                                                      content_type='image/jpg')
        serializer = FileSerializer(data=file_other_data)
        serializer.is_valid()
        assert 'Only one of' in serializer.errors['non_field_errors'][0]

    def test_created_by_is_set_on_instance(self, api_rf, student1, file_other_data):
        request = mock.Mock(user=student1.user)
        serializer = FileSerializer(data=file_other_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        assert instance.created_by == student1 and instance.modified_by == student1, \
            "Creator and modifier are set on instance"

    def test_modified_by_is_set_on_instance(self, api_rf, student1, student2, file_other_data, students1_file):
        request = mock.Mock(user=student2.user)
        serializer = FileSerializer(data=file_other_data, instance=students1_file, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        assert instance.created_by == student1 and instance.modified_by == student2, \
            "Creator is the same and modifier is set as another student"
