import datetime
from random import randint

import factory
from django.utils.text import slugify

from ..subject.models import (
    Exam,
    FieldOfStudy,
    FieldOfStudyOfAgeGroup,
    Resource,
    ResourceCategoryChoices,
    Subject,
    SubjectOfAgeGroup,
)


class FieldOfStudyFactory(factory.django.DjangoModelFactory):
    name = factory.sequence(lambda n: f"field{n}")
    slug = factory.LazyAttribute(lambda o: f"{slugify(o.name)}")

    class Meta:
        model = FieldOfStudy


class FieldOfStudyOfAgeGroupFactory(factory.django.DjangoModelFactory):
    field_of_study = factory.SubFactory(FieldOfStudyFactory)
    students_start_year = factory.LazyAttribute(
        lambda n: datetime.datetime.now().year - 1
    )

    class Meta:
        model = FieldOfStudyOfAgeGroup


class SubjectFactory(factory.django.DjangoModelFactory):
    name = factory.sequence(lambda n: f"subject{n}")
    semester = factory.LazyAttribute(lambda n: randint(1, 6))
    general_description = "description"
    module_code = factory.sequence(lambda n: f"module{n}")
    field_of_study = factory.SubFactory(FieldOfStudyFactory)

    class Meta:
        model = Subject


class SubjectOfAgeGroupFactory(factory.django.DjangoModelFactory):
    subject = factory.SubFactory(SubjectFactory)
    field_age_group = factory.SubFactory(FieldOfStudyOfAgeGroupFactory)

    class Meta:
        model = SubjectOfAgeGroup


class ExamFactory(factory.django.DjangoModelFactory):
    subject_group = factory.SubFactory(SubjectOfAgeGroupFactory)
    starts_at = datetime.datetime.now() + datetime.timedelta(days=30)

    class Meta:
        model = Exam


class ResourceFactory(factory.django.DjangoModelFactory):
    name = factory.sequence(lambda n: f"Resource {n}")
    subject = factory.SubFactory(SubjectFactory)
    category = ResourceCategoryChoices.OTHER

    class Meta:
        model = Resource
