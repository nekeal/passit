import csv
import dataclasses

from .models import CustomUser, MembershipTypeChoices
from .serializers import StudentsImportSerializer
from ..subject.tests.fixtures import field_age_group


@dataclasses.dataclass
class Student:
    first_name: str
    last_name: str
    username: str
    password: str

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class StudentImportService:

    def __init__(self, field_age_group, membership_type):
        self.field_age_group = field_age_group
        self.membership_type = membership_type
        self.student_create_result = {'valid': [], 'invalid': []}

    def create_from_file(self, file):
        csv_reader = csv.reader(file)
        for line in csv_reader:
            password = CustomUser.objects.make_random_password(8)
            student = Student(*line, password)
            serializer = StudentsImportSerializer(data=dataclasses.asdict(student))
            if serializer.is_valid():
                serializer.save(field_age_group=field_age_group, type=MembershipTypeChoices.NORMAL)
                self.student_create_result['valid'].append({'student': student})
            else:
                self.student_create_result['invalid'].append({'errors': serializer.errors, 'student': student})

    def print_report(self):
        print('Created:')
        for student in self.student_create_result['valid']:
            print(f'{student["student"].get_full_name()} - {student["student"].username}:{student["student"].password}')
        print("Failed to create:")
        for student in self.student_create_result['invalid']:
            print(f'{student["student"].get_full_name()} - {student["errors"]}')

    def get_result(self):
        return self.student_create_result

    def create_from_filename(self, filename):
        with open(filename) as f:
            self.create_from_file(f)
