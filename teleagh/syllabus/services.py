from collections import Counter
from typing import Tuple, List, Set

from .utils import SyllabusClient, SubjectAdapter
from ..lecturers.models import LecturerOfSubjectOfAgeGroup
from ..lecturers.serializers import LecturerSyllabusImportSerializer
from ..subject.models import FieldOfStudy, FieldOfStudyOfAgeGroup, SubjectOfAgeGroup
from ..subject.serializers import SubjectSyllabusImportSerializer


class SyllabusStartNewYearService:

    def __init__(self, faculty: str, age_group: str, field_of_study_slug):
        self.faculty = faculty
        self.age_group = age_group
        self.field_of_study = FieldOfStudy.objects.get(slug=field_of_study_slug)
        self.field_age_group = None
        self.start_year = self.get_start_year()
        self.client = SyllabusClient()
        self.subjects_parsed_data = []
        self.subject_instances = []
        self.subject_age_groups_create_result: List[Tuple[SubjectOfAgeGroup, bool]] = []
        self.lecturer_age_groups_create_result: Set[Tuple[LecturerOfSubjectOfAgeGroup, bool]] = set()
        self.report = []

    def get_start_year(self):
        try:
            return int(self.age_group.split('-')[0])
        except Exception as e:
            type(e)(e.message + f"\n {self.age_group}")

    def add_subjects_of_age_group_create_result_to_report(self):
        subject_age_group_summary = Counter([result[1] for result in self.subject_age_groups_create_result])
        old_subject_groups = subject_age_group_summary.get(False, 0)
        new_subject_groups = subject_age_group_summary.get(True, 0)
        self.report.append(f'{new_subject_groups} new subjects created, {old_subject_groups} already exist')

    def add_lecturers_of_age_group_create_result_to_report(self):
        lecturer_age_group_summary = Counter([result[1] for result in self.lecturer_age_groups_create_result])
        old_lecturer_groups = lecturer_age_group_summary.get(False, 0)
        new_lecturer_groups = lecturer_age_group_summary.get(True, 0)
        self.report.append(f'{new_lecturer_groups} new lecturers of age group created, {old_lecturer_groups}'
                           f' already exist')

    def get_report(self):
        return self.report

    def print_report(self):
        print('\n'.join(self.report))

    def create_field_age_group(self):
        field_age_group, created = FieldOfStudyOfAgeGroup.objects.get_or_create(field_of_study=self.field_of_study,
                                                                                students_start_year=self.start_year)
        self.report.append(f'{"Created" if created else "Retrieved"} field age group for {self.field_of_study.name}'
                           f'for year {self.start_year}')
        self.field_age_group = field_age_group

    def create_subjects_of_age_group(self):
        subjects_raw_data = self.client.get_full_subjects_data(self.age_group, self.faculty, self.field_of_study.slug)
        self.subjects_parsed_data = [SubjectAdapter(self.field_of_study, subject).get_data() for subject in
                                     subjects_raw_data.values()]
        subject_serializer = SubjectSyllabusImportSerializer(data=self.subjects_parsed_data, many=True)
        subject_serializer.is_valid(raise_exception=True)
        self.subject_instances = subject_serializer.save()
        self.subject_age_groups_create_result = [
            SubjectOfAgeGroup.objects.get_or_create(subject=subject_instance, field_age_group=self.field_age_group)
            for subject_instance in self.subject_instances
        ]
        self.add_subjects_of_age_group_create_result_to_report()

    def create_lecturers_of_age_group(self):
        for i in range(len(self.subject_instances)):
            lecturer_serializer = LecturerSyllabusImportSerializer(data=self.subjects_parsed_data[i]['lecturers'],
                                                                   many=True)
            lecturer_serializer.is_valid(raise_exception=False)
            lecturer_instances = lecturer_serializer.save()
            lecturers_of_age_groups: List[Tuple[LecturerOfSubjectOfAgeGroup, bool]] = [
                LecturerOfSubjectOfAgeGroup.objects.get_or_create(
                    lecturer=lecturer, subject_group=self.subject_age_groups_create_result[i][0])
                for lecturer in lecturer_instances
            ]
            self.lecturer_age_groups_create_result.update(lecturers_of_age_groups)
        self.add_lecturers_of_age_group_create_result_to_report()
