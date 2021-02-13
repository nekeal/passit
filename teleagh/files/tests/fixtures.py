import pytest
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from teleagh.files.factories import FileFactory


@pytest.fixture
def file(db):
    return FileFactory(name='file')


@pytest.fixture
def students1_file(student1):
    return FileFactory(created_by=student1, modified_by=student1)


@pytest.fixture
def file_other_data():
    return {
        'name': 'file',
        'other': SimpleUploadedFile('f.txt', b'text')
    }

@pytest.fixture
def file_image_data(image_file):
    return {
        'name': 'image',
        'other': SimpleUploadedFile('image.jpg', image_file.read(), content_type='image/jpg')
    }


@pytest.fixture
def image_file() -> File:
    return FileFactory.build().image.file
