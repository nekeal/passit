from passit.accounts.models import Membership
from passit.accounts.serializers import StudentsImportSerializer


class TestStudentImportSerializer:
        
    @staticmethod
    def get_valid_data():
        return {
            "username": "username",
            "password": "password",
            "first_name": "John",
            "last_name": "Smith",
        }

    def test_all_fields_are_required(self):
        serializer = StudentsImportSerializer()
        for field in serializer.get_fields().values():
            assert field.required

    def test_create_student(self, field_age_group):
        
        serializer = StudentsImportSerializer(data=self.get_valid_data())
        serializer.is_valid(raise_exception=True)
        user = serializer.save(field_age_group=field_age_group)
        assert user.profile is not None
        assert Membership.objects.get(profile=user.profile).field_age_group == field_age_group
    
    def test_validate_unique_username(self, user_profile1, field_age_group):
        valid_data = self.get_valid_data()
        valid_data["username"] = user_profile1.user.username
        serializer = StudentsImportSerializer(data=valid_data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors
