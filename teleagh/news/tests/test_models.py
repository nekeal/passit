from ...accounts.factories import MembershipFactory
from ..factories import NewsFactory
from ..models import News
from ...subject.factories import SubjectOfAgeGroupFactory


def test_get_news_by_profile(user_profile_with_membership, subject_group):
    expected_news = NewsFactory.create_batch(3, subject_group=subject_group)
    NewsFactory.create_batch(2, subject_group=SubjectOfAgeGroupFactory())
    user_news = News.objects.get_by_profile(user_profile_with_membership)
    assert len(user_news) == 3, "method gets wrong news for user"
    assert list(user_news) == expected_news, "method gets wrong news for user"


def test_get_news_by_profile_with_multiple_memberships(user_profile_with_membership, subject_group):
    another_subject_of_age_group = SubjectOfAgeGroupFactory()
    MembershipFactory(profile=user_profile_with_membership,
                      field_age_group=another_subject_of_age_group.field_age_group)
    expected_news = NewsFactory.create_batch(1, subject_group=subject_group)
    expected_news += NewsFactory.create_batch(1, subject_group=another_subject_of_age_group)
    NewsFactory.create_batch(2, subject_group=SubjectOfAgeGroupFactory())
    user_news = News.objects.get_by_profile(user_profile_with_membership)
    assert len(user_news) == 2, "method gets wrong number of news for user"
    assert list(user_news) == expected_news, "method gets wrong news for user"
