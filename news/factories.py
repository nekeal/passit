import factory

from news.models import News
from subject.factories import SubjectOfAgeGroupFactory


class NewsFactory(factory.DjangoModelFactory):
    title = factory.sequence(lambda n: f"Title {n}")
    subject_group = factory.SubFactory(SubjectOfAgeGroupFactory)
    content = ""

    class Meta:
        model = News
