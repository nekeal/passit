import pytest
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from passit.events.models import EventCategoryChoices
from passit.events.serializers import EventSerializer
from passit.subject.factories import (
    FieldOfStudyOfAgeGroupFactory,
    SubjectOfAgeGroupFactory,
)
from passit.subject.serializers import (
    FieldOfStudyOfAgeGroupSerializer,
    SubjectOfAgeGroupSerializer,
)


class TestEventSerializer:
    @staticmethod
    def get_minimal_valid_data(field_age_group, **kwargs):
        data = {
            "name": "event_name",
            "category": EventCategoryChoices.OTHER,
            "due_date": str(timezone.now()),
            "field_age_group": field_age_group.id,
        }
        data.update(**kwargs)
        return data

    def test_get_minimal_valid_data(self, field_age_group):
        serializer = EventSerializer(data=self.get_minimal_valid_data(field_age_group))
        serializer.is_valid(raise_exception=True)

    @pytest.mark.parametrize(
        "field_name,serializer_class",
        (
            ("field_age_group", FieldOfStudyOfAgeGroupSerializer),
            ("subject_group", SubjectOfAgeGroupSerializer),
        ),
    )
    def test_expandable_fields(self, field_name, serializer_class):
        serializer = EventSerializer(
            expand=[
                field_name,
            ]
        )
        field_config = serializer._expandable_fields[field_name]
        assert serializer.expanded_fields == [
            field_name,
        ]
        assert field_config[0] == serializer_class

    @pytest.mark.parametrize(
        "field_name,is_required",
        (
            ("id", False),
            ("name", True),
            ("description", False),
            ("category", True),
            ("due_date", True),
            ("field_age_group", True),
            ("subject_group", False),
            ("created_by", False),
            ("modified_by", False),
            ("created_by_profile", False),
            ("modified_by_profile", False),
        ),
    )
    def test_required_fields(self, field_name, is_required):
        assert EventSerializer().fields[field_name].required is is_required

    @pytest.mark.parametrize('field_age_group_id', (1, "1"))
    @pytest.mark.parametrize('subject_group_id', (1, "1"))
    def test_validate_correct_subject_group(self, subject_group_id, field_age_group_id):
        field_age_group = FieldOfStudyOfAgeGroupFactory.build()
        subject_group = SubjectOfAgeGroupFactory.build(field_age_group=field_age_group)
        subject_group.field_age_group_id = field_age_group_id
        serializer = EventSerializer(
            data={
                'name': 'name',
                'category': EventCategoryChoices.OTHER,
                'field_age_group': field_age_group_id,
                'subject_group': subject_group_id,
            }
        )
        assert serializer.validate_subject_group(subject_group) == subject_group

    def test_subject_not_match_field_age_group(self):
        subject_group = SubjectOfAgeGroupFactory.build(id=1, field_age_group_id=2)
        serializer = EventSerializer(
            data={
                'name': 'name',
                'category': EventCategoryChoices.OTHER,
                'field_age_group': 1,
                'subject_group': 1,
            }
        )
        with pytest.raises(ValidationError):
            serializer.validate_subject_group(subject_group)

    def test_field_of_study_is_omitted_in_subject_group_serializer(self):
        assert (
            EventSerializer()._expandable_fields["subject_group"][1]["omit"]
            == "subject.field_of_study"
        )
