import datetime
from random import randint
import factory

from subject.models import FieldOfStudies, Subject, SubjectOfAgeGroup, Resource, Exam


class FieldOfStudiesFactory(factory.DjangoModelFactory):

    class Meta:
        model = FieldOfStudies

    name = factory.sequence(lambda n: f'field{n}')


class SubjectFactory(factory.DjangoModelFactory):

    class Meta:
        model = Subject

    name = factory.sequence(lambda n: f'subject{n}')
    semester = factory.LazyAttribute(lambda n: randint(1, 6))
    general_description = "opis"
    field_of_studies = factory.SubFactory(FieldOfStudiesFactory)


class SubjectOfAgeGroupFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectOfAgeGroup

    subject = factory.SubFactory(SubjectFactory)
    students_start_year = factory.LazyAttribute(lambda n: datetime.datetime.now().year - 1)


class ExamFactory(factory.DjangoModelFactory):

    class Meta:
        model = Exam

    subject_group = factory.SubFactory(SubjectOfAgeGroupFactory)
    starts_at = datetime.datetime.now() + datetime.timedelta(days=30)


class ResourceFactory(factory.DjangoModelFactory):

    class Meta:
        model = Resource

    name = factory.sequence(lambda n: f"Resource {n}")
    subject = factory.SubFactory(Subject)
