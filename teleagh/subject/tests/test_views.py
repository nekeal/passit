import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate

from teleagh.files.factories import FileFactory
from teleagh.files.models import File
from teleagh.subject.models import Resource
from teleagh.subject.views import ResourceViewSet


@pytest.fixture
def resource_list_view():
    return ResourceViewSet.as_view({'get': 'list', 'post': 'create'})


@pytest.fixture
def resource_detail_view():
    return ResourceViewSet.as_view({'get': 'retrieve', 'post': 'create', 'delete': 'destroy', 'put': 'update'})

# ---ResourceViewSet---


def test_student_can_create_resource_without_files(api_rf, resource_list_view, student1, resource_data_without_files):
    request = api_rf.post(reverse('api:resource-list'), data=resource_data_without_files)
    force_authenticate(request, student1.user)
    response = resource_list_view(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert Resource.objects.count() == 1


def test_student_can_create_resource_with_files(api_rf, resource_list_view, student1, resource_data_without_files):
    file = FileFactory(created_by=student1)
    resource_data_with_files = resource_data_without_files.copy()
    resource_data_with_files['files'] = [file.id]
    request = api_rf.post(reverse('api:resource-list'), data=resource_data_with_files)
    force_authenticate(request, student1.user)
    response = resource_list_view(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert Resource.objects.count() == 1
    assert list(Resource.objects.first().files.values('id')) == [{'id': file.id}]


def test_student_can_create_resource_using_own_files(api_rf, resource_list_view, student1, students1_file,
                                                           resource_data_without_files):
    resource_data_without_files['files'] = [students1_file.id]
    request = api_rf.post(reverse('api:file-list'), data=resource_data_without_files)
    force_authenticate(request, student1.user)
    response = resource_list_view(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert File.objects.count() == 1

def test_student_cant_create_resource_using_someones_files(api_rf, resource_list_view, student2, students1_file,
                                                           resource_data_without_files):
    resource_data_without_files['files'] = [students1_file.id]
    request = api_rf.post(reverse('api:file-list'), data=resource_data_without_files)
    force_authenticate(request, student2.user)
    response = resource_list_view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid pk" in response.data['files'][0]
