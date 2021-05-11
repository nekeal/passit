import factory

from ..subject.factories import SubjectOfAgeGroupFactory
from .models import Lecturer, LecturerOfSubjectOfAgeGroup


class LecturerFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = Lecturer


class LecturerOfSubjectOfAgeGroupFactory(factory.django.DjangoModelFactory):
    lecturer = factory.SubFactory(LecturerFactory)
    subject_group = factory.SubFactory(SubjectOfAgeGroupFactory)

    class Meta:
        model = LecturerOfSubjectOfAgeGroup
