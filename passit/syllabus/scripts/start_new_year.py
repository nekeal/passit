import argparse

from ..services import SyllabusStartNewYearService
from ..utils import SyllabusClient

parser = argparse.ArgumentParser(
    description='Syllabus import',
)
parser.add_argument(
    '--age-group',
    help='Specify age-group to fetch in format <year>-<year>',
    required=False,
    default='2018-2019',
)
parser.add_argument(
    '--faculty',
    help='Specify faculty to fetch data from',
    required=False,
    default='wieit',
)
parser.add_argument(
    '--field-of-study',
    help='Specify field of study to fetch subjects from',
    required=False,
    default='stacjonarne-teleinformatyka',
)

client = SyllabusClient()


def run(*args):
    args = args[0].split(" ") if len(args) else args
    print(args)
    parsed_args = parser.parse_args(args)
    service = SyllabusStartNewYearService(
        parsed_args.faculty, parsed_args.age_group, parsed_args.field_of_study
    )
    service.create_field_age_group()
    service.create_subjects_of_age_group()
    service.create_lecturers_of_age_group()
    service.print_report()
