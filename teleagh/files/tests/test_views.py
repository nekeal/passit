import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate

from teleagh.common.utils import setup_view
from teleagh.files.factories import FileFactory
from teleagh.files.models import File
from teleagh.files.views import FileViewSet


@pytest.fixture
def file_list_view():
    return FileViewSet.as_view({'get': 'list', 'post': 'create'})


@pytest.fixture
def file_detail_view():
    return FileViewSet.as_view({'get': 'retrieve', 'post': 'create', 'delete': 'destroy', 'put': 'update'})


class TestFileViewSet:

    def test_user_without_profile_cant_access_view(self, api_rf, file_list_view, user1):
        request = api_rf.get(reverse('api:file-list'))
        force_authenticate(request, user1)
        response = file_list_view(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_without_membership_cant_access_view(self, api_rf, file_list_view, user_profile1):
        request = api_rf.get(reverse('api:file-list'))
        force_authenticate(request, user_profile1.user)
        response = file_list_view(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_student_can_access_view(self, api_rf, file_list_view, student1):
        request = api_rf.get(reverse('api:file-list'))
        force_authenticate(request, student1.user)
        response = file_list_view(request)
        assert response.status_code == status.HTTP_200_OK

    def test_files_are_filtered_by_user(self, api_rf, student1, student2, students1_file):
        FileFactory(created_by=student2)
        request = api_rf.get(reverse('api:file-list'))
        request.user = student1.user
        view = setup_view(FileViewSet(), request)
        assert list(view.get_queryset()) == list(File.objects.filter_by_profile(student1))

    def test_student_can_create_file_with_other(self, api_rf, file_list_view, student1, file_other_data):
        request = api_rf.post(reverse('api:file-list'), data=file_other_data)
        force_authenticate(request, student1.user)
        response = file_list_view(request)
        assert response.status_code == status.HTTP_201_CREATED
        assert File.objects.count() == 1

    def test_student_can_create_file_with_image(self, api_rf, file_list_view, student1, file_image_data):
        request = api_rf.post(reverse('api:file-list'), data=file_image_data)
        force_authenticate(request, student1.user)
        response = file_list_view(request)
        assert response.status_code == status.HTTP_201_CREATED
        assert File.objects.count() == 1

    def test_owner_can_edit_his_files(self, api_rf, file_detail_view, student1, students1_file, file_other_data):
        request = api_rf.put(reverse('api:file-list'), data=file_other_data, args=(students1_file.id,))
        force_authenticate(request, student1.user)
        response = file_detail_view(request, pk=students1_file.id)
        students1_file.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert students1_file.name == 'file'

    def test_privileged_cant_edit_someones_files(self, api_rf, file_detail_view, student1, students1_file, file_other_data,
                                                 representative_profile):
        request = api_rf.put(reverse('api:file-list'), data=file_other_data, args=(students1_file.id,))
        force_authenticate(request, representative_profile.user)
        response = file_detail_view(request, pk=students1_file.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_student_can_delete_his_files(self, api_rf, file_detail_view, student1, students1_file, file_other_data):
        request = api_rf.delete(reverse('api:file-list'), args=(students1_file.id,))
        force_authenticate(request, student1.user)
        response = file_detail_view(request, pk=students1_file.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not File.objects.filter(id=students1_file.id).exists()

