import pytest
# --- FileSerializer ---
from django.core.files.uploadedfile import SimpleUploadedFile

from teleagh.files.serializers import FileSerializer


def test_image_or_other_should_be_set(api_rf, file_other_data):
    file_other_data.pop('other')
    serializer = FileSerializer(data=file_other_data)
    serializer.is_valid()
    assert 'One of' in serializer.errors['non_field_errors'][0]


@pytest.mark.django_db
def test_image_or_other_cant_be_set_together(api_rf, file_other_data, image_file):
    file_other_data['image'] = SimpleUploadedFile('a.jpg', content=image_file.read(),
                                                  content_type='image/jpg')
    serializer = FileSerializer(data=file_other_data)
    serializer.is_valid()
    assert 'Only one of' in serializer.errors['non_field_errors'][0]

