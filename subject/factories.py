import datetime
from random import randint
import factory

from subject.models import FieldOfStudy, Subject, SubjectOfAgeGroup, Resource, Exam


class FieldOfStudyFactory(factory.DjangoModelFactory):
    name = factory.sequence(lambda n: f'field{n}')

    class Meta:
        model = FieldOfStudy


class SubjectFactory(factory.DjangoModelFactory):
    name = factory.sequence(lambda n: f'subject{n}')
    semester = factory.LazyAttribute(lambda n: randint(1, 6))
    general_description = "description"
    field_of_study = factory.SubFactory(FieldOfStudyFactory)

    class Meta:
        model = Subject


class SubjectOfAgeGroupFactory(factory.DjangoModelFactory):
    subject = factory.SubFactory(SubjectFactory)
    students_start_year = factory.LazyAttribute(lambda n: datetime.datetime.now().year - 1)

    class Meta:
        model = SubjectOfAgeGroup


class ExamFactory(factory.DjangoModelFactory):
    subject_group = factory.SubFactory(SubjectOfAgeGroupFactory)
    starts_at = datetime.datetime.now() + datetime.timedelta(days=30)

    class Meta:
        model = Exam


class ResourceFactory(factory.DjangoModelFactory):
    name = factory.sequence(lambda n: f"Resource {n}")
    subject = factory.SubFactory(Subject)

    class Meta:
        model = Resource
