from ..factories import NewsFactory
from ..models import News
from ...accounts.factories import MembershipFactory
from ...subject.factories import FieldOfStudyOfAgeGroupFactory, SubjectOfAgeGroupFactory


class TestNews:
    def test_str_method(self):
        news = NewsFactory.build()
        assert str(news) == news.title


class TestNewsManager:
    def test_get_news_by_profile(self, student1, field_age_group):
        expected_news = NewsFactory.create_batch(3, field_age_group=field_age_group)
        NewsFactory.create_batch(2, field_age_group=FieldOfStudyOfAgeGroupFactory())
        user_news = News.objects.get_by_profile(student1)
        assert len(user_news) == 3, "method gets wrong news for user"
        assert set(user_news) == set(expected_news), "method gets wrong news for user"

    def test_get_news_by_profile_with_multiple_memberships(
        self, student1, subject_group
    ):
        another_subject_of_age_group = SubjectOfAgeGroupFactory()
        MembershipFactory(
            profile=student1,
            field_age_group=another_subject_of_age_group.field_age_group,
        )
        expected_news = NewsFactory.create_batch(1, subject_group=subject_group)
        expected_news += NewsFactory.create_batch(
            1, subject_group=another_subject_of_age_group
        )
        NewsFactory.create_batch(2, subject_group=SubjectOfAgeGroupFactory())
        user_news = News.objects.get_by_profile(student1)
        assert len(user_news) == 2, "method gets wrong number of news for user"
        assert list(user_news) == expected_news, "method gets wrong news for user"
