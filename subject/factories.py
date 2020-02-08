import datetime
from random import randint
import factory

from subject.models import FieldOfStudies, Subject, SubjectOfAgeGroup, Resource, Exam


class FieldOfStudiesFactory(factory.DjangoModelFactory):
    name = factory.sequence(lambda n: f'field{n}')

    class Meta:
        model = FieldOfStudies


class SubjectFactory(factory.DjangoModelFactory):

    name = factory.sequence(lambda n: f'subject{n}')
    semester = factory.LazyAttribute(lambda n: randint(1, 6))
    general_description = "description"
    field_of_studies = factory.SubFactory(FieldOfStudiesFactory)

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
