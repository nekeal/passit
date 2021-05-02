import argparse
import dataclasses

from ..models import MembershipTypeChoices
from ..services import StudentImportService
from ...subject.models import FieldOfStudyOfAgeGroup

parser = argparse.ArgumentParser(description='Syllabus import')
parser.add_argument('filename',
                    help='Csv filename which contains users to be created',
                    )
parser.add_argument('--start-year',
                    help='Specify age-group to fetch in format <year>-<year>',
                    required=False,
                    default='2018',
                    type=int
                    )
parser.add_argument('--field-of-study',
                    help='Specify field of study to fetch subjects from',
                    required=False,
                    default='stacjonarne-teleinformatyka'
                    )


@dataclasses.dataclass
class Student:
    first_name: str
    last_name: str
    username: str
    password: str


def run(*args):
    args = args[0].split(" ") if len(args) else args
    parsed_args = parser.parse_args(args)
    field_age_group = FieldOfStudyOfAgeGroup.objects.get(field_of_study__slug=parsed_args.field_of_study,
                                                         students_start_year=parsed_args.start_year)
    service = StudentImportService(field_age_group, MembershipTypeChoices.NORMAL)
    service.create_from_filename('users.csv')
    service.print_report()
    # student_create_result = {'valid': [], 'invalid': []}
    # with open(parsed_args.filename, 'r') as f:
    #     csv_reader = csv.reader(f)
    #     for line in csv_reader:
    #         password = CustomUser.objects.make_random_password(8)
    #         student = Student(*line, password)
    #         serializer = StudentsImportSerializer(data=dataclasses.asdict(student))
    #         if serializer.is_valid():
    #             serializer.save(field_age_group=field_age_group, type=MembershipTypeChoices.NORMAL)
    #             student_create_result['valid'].append({'student': student})
    #         else:
    #             student_create_result['invalid'].append({'errors': serializer.errors, 'student': student})
    #
    #     from pprint import pprint
    #     pprint(student_create_result)
    #     print(student_create_result['invalid'][0])
