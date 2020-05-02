from unittest import mock

from ..serializers import FieldOfStudyOfAgeGroupSerializer, ResourceBaseSerializer


# --- FieldOfAgeGroupSerializer ---


def test_can_serialize_field_age_group(field_age_group, field_age_group_data):
    serializer = FieldOfStudyOfAgeGroupSerializer(field_age_group)
    assert serializer.data == {
        'id': field_age_group.id,
        'field_of_study': field_age_group.field_of_study.id,
        'students_start_year': 2018
    }


def test_can_create_field_age_group(db, field_age_group_data):
    serializer = FieldOfStudyOfAgeGroupSerializer(data=field_age_group_data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    assert (instance.field_of_study.id, instance.students_start_year)\
        == (field_age_group_data['field_of_study'], field_age_group_data['students_start_year'])


# --- ResourceSerializer ---

def test_resource_owned_model_serializer(resource_data_without_files, api_rf, user_profile1, user_profile2):
    request_user1 = mock.Mock()
    request_user1.user = user_profile1.user
    request_user2 = mock.Mock()
    request_user2.user = user_profile2.user
    serializer = ResourceBaseSerializer(data=resource_data_without_files, context={'request': request_user1})
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    assert instance.created_by == user_profile1, "Creator is set on instace"
    assert instance.modified_by == user_profile1, "Modifier is set on instance"
    serializer = ResourceBaseSerializer(data=resource_data_without_files, instance=instance, context={'request': request_user2})
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    assert instance.created_by == user_profile1, "Creator is unchanged on instance"
    assert instance.modified_by == user_profile2, "Modifier is changed on instance"
