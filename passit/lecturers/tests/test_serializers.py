import pytest

from ..factories import LecturerFactory
from ..serializers import LecturerBaseSerializer, LecturerSyllabusImportSerializer


class TestLecturerBaseSerializer:
    @pytest.mark.parametrize(
        "field_name,is_required",
        (
            ("id", False),
            ("first_name", True),
            ("last_name", True),
            ("title", False),
            ("contact", False),
            ("consultations", False),
        ),
    )
    def test_required_fields(self, field_name, is_required):
        assert LecturerBaseSerializer().fields[field_name].required is is_required


class TestLecturerSyllabusImportSerializer:
    def setup_method(self):
        self.data = {"first_name": "John", "last_name": "Smith", "title": "dr."}

    @pytest.mark.django_db
    def test_create_does_not_duplicate_lecturer(self):
        lecturer = LecturerFactory(**self.data)
        serializer = LecturerSyllabusImportSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        assert lecturer == instance

    @pytest.mark.django_db
    def test_create_lecturer(self):
        lecturer = LecturerFactory(**self.data)
        self.data["first_name"] = "Jack"
        serializer = LecturerSyllabusImportSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        assert lecturer != instance
