import factory

from .models import Lecturer, LecturerOfSubjectOfAgeGroup
from ..subject.factories import SubjectOfAgeGroupFactory


class LecturerFactory(factory.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    class Meta:
        model = Lecturer


class LecturerOfSubjectOfAgeGroupFactory(factory.DjangoModelFactory):
    lecturer = factory.SubFactory(LecturerFactory)
    subject_group = factory.SubFactory(SubjectOfAgeGroupFactory)

    class Meta:
        model = LecturerOfSubjectOfAgeGroup
