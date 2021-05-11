import json
from urllib.parse import urljoin

import requests

from passit.subject.models import FieldOfStudy


class LecturerAdapter:
    def __init__(self, json_data_from_syllabus):
        data = json_data_from_syllabus
        self.lecturer_data = {
            "first_name": data["name"],
            "last_name": data["surname"],
            "title": data["employee_title"] or "",
        }

    def get_data(self):
        return self.lecturer_data


class SubjectAdapter:
    def __init__(self, field_of_study: FieldOfStudy, json_data_from_syllabus):
        self.initial_data = json_data_from_syllabus
        self.subject_data = {
            "module_code": self.initial_data["module_code"],
            "name": self.initial_data["name"],
            "general_description": self.initial_data["description"].strip(),
            "semester": self.initial_data["semester"],
            "category": self.initial_data["category"].strip(),
            "field_of_study": field_of_study.id,
            "lecturers": self.get_lecturers(),
        }

    def get_lecturers(self):
        lecturers = [
            LecturerAdapter(lecturer["teacher"]).get_data()
            for lecturer in self.initial_data["teachers"]
        ]
        return lecturers

    def save_data(self, filename="subjects_list.json"):
        with open(filename, "a+") as f:
            f.write(json.dumps(self.subject_data) + "\n")

    def get_data(self):
        return self.subject_data


class SyllabusClient:
    BASE_URL = "https://syllabuskrk.agh.edu.pl"
    FIELDS_OF_STUDY_LIST_BASE_URL = urljoin(
        BASE_URL, "/{age_group}/magnesite/api/faculties/{faculty}/study_plans"
    )
    SUBJECTS_LIST_BASE_URL = urljoin(
        BASE_URL,
        "/{age_group}/magnesite/api/faculties/{faculty}/study_plans/{field_of_study}",
    )
    SUBJECTS_LIST_WITH_DETAILS_URL = "/".join(
        [
            SUBJECTS_LIST_BASE_URL,
            "modules/?fields=description,teachers,module-owner,"
            "credit-conditions,module_activities,module-code",
        ]
    )

    def __init__(self, language="pl"):
        self.session = requests.Session()
        headers = {"accept-language": language}
        self.session.headers.update(headers)

    @classmethod
    def _get_field_of_study_url(cls, age_group, faculty):
        return cls.FIELDS_OF_STUDY_LIST_BASE_URL.format(age_group, faculty)

    @classmethod
    def _get_subject_list_url(cls, age_group, faculty, field_of_study):
        return cls.SUBJECTS_LIST_BASE_URL.format(
            age_group=age_group, faculty=faculty, field_of_study=field_of_study
        )

    @classmethod
    def _get_subject_list_details_url(cls, age_group, faculty, field_of_study):
        return cls.SUBJECTS_LIST_WITH_DETAILS_URL.format(
            age_group=age_group, faculty=faculty, field_of_study=field_of_study
        )

    def _merge_subjects_data(self, common_data, detail_data):
        merged_data = {}
        for semester in common_data:
            semester_number = semester["number"]
            for group in semester["groups"]:
                group_name = group["name"]
                for subject in group["modules"]:
                    merged_data[subject["module_code"]] = subject
                    merged_data[subject["module_code"]]["semester"] = semester_number
                    merged_data[subject["module_code"]]["category"] = group_name
        for subject in detail_data:
            assignment = subject["assignment"]
            merged_data[assignment["module_code"]].update(assignment["module"])
        return merged_data

    def get_common_subjects_data(self, age_group, faculty, field_of_study_slug):
        url = self._get_subject_list_url(age_group, faculty, field_of_study_slug)
        response = self.session.get(url)
        try:
            data = response.json()["syllabus"]["study_plan"]["semesters"]
        except json.JSONDecodeError:
            raise ValueError(f"Failed during parsing response {response.content}")
        return data

    def get_detail_subjects_data(self, age_group, faculty, field_of_study):
        url = self._get_subject_list_details_url(age_group, faculty, field_of_study)
        response = self.session.get(url)
        try:
            data = response.json()["syllabus"]["assignments"]
        except json.JSONDecodeError:
            raise ValueError(f"Failed during parsing response {response.content}")
        return data

    def get_full_subjects_data(self, age_group, faculty, field_of_study):
        common_data = self.get_common_subjects_data(age_group, faculty, field_of_study)
        detail_data = self.get_detail_subjects_data(age_group, faculty, field_of_study)
        return self._merge_subjects_data(common_data, detail_data)
