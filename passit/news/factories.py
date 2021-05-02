import factory

from .models import News
from ..subject.factories import SubjectOfAgeGroupFactory


class NewsFactory(factory.DjangoModelFactory):
    title = factory.sequence(lambda n: f'Title {n}')
    subject_group = factory.SubFactory(SubjectOfAgeGroupFactory)
    field_age_group = factory.LazyAttribute(lambda o: o.subject_group.field_age_group)
    content = ''

    class Meta:
        model = News
