import pytest

from unittest import mock

from subject.serializers import FieldOfStudyOfAgeGroupSerializer


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
