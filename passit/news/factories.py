import factory

from ..subject.factories import SubjectOfAgeGroupFactory
from .models import News


class NewsFactory(factory.django.DjangoModelFactory):
    title = factory.sequence(lambda n: f"Title {n}")
    subject_group = factory.SubFactory(SubjectOfAgeGroupFactory)
    field_age_group = factory.LazyAttribute(lambda o: o.subject_group.field_age_group)
    content = ""

    class Meta:
        model = News
