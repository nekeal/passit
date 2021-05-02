import pytest

from passit.subject.factories import SubjectFactory, FieldOfStudyFactory, SubjectOfAgeGroupFactory, \
    FieldOfStudyOfAgeGroupFactory, ResourceFactory
from passit.subject.models import ResourceCategoryChoices


@pytest.fixture
def field_of_study(db):
    return FieldOfStudyFactory(name='ICT', slug="ICT")


@pytest.fixture
def field_age_group(db, field_of_study):
    return FieldOfStudyOfAgeGroupFactory(field_of_study=field_of_study, students_start_year=2018)


@pytest.fixture
def subject(db, field_of_study):
    return SubjectFactory(name='PT', semester=1, field_of_study=field_of_study)


@pytest.fixture
def resource(subject):
    return ResourceFactory(name="Resource", subject=subject)

@pytest.fixture
def subject_group(db, subject, field_age_group):
    return SubjectOfAgeGroupFactory(subject=subject, field_age_group=field_age_group)


@pytest.fixture
def field_age_group_data(field_of_study):
    return {
        'field_of_study': field_of_study.id,
        'students_start_year': 2018,
    }


@pytest.fixture
def resource_data(subject):
    return {
        'name': 'resource',
        'subject': subject.id,
        'category': ResourceCategoryChoices.OTHER,
    }
