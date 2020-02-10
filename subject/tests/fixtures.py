import pytest

from subject.factories import SubjectFactory, FieldOfStudyFactory, SubjectOfAgeGroupFactory


@pytest.fixture
def field_of_study(db):
    return FieldOfStudyFactory(name='ICT', slug="ICT")


@pytest.fixture
def subject(db, field_of_study):
    return SubjectFactory(name='PT', semester=1, field_of_study=field_of_study)


@pytest.fixture
def subject_group(db, subject):
    return SubjectOfAgeGroupFactory(subject=subject)
