import pytest

from accounts.factories import MembershipFactory
from accounts.models import MembershipTypeChoices
from news.factories import NewsFactory
from news.models import News
from subject.factories import SubjectOfAgeGroupFactory


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


@pytest.mark.parametrize('membership_type,expected_value', ((MembershipTypeChoices.NORMAL, False),
                                                 (MembershipTypeChoices.MODERATOR, True),
                                                 (MembershipTypeChoices.REPRESENTATIVE, True)))
def test_is_privileged_method(membership_type, expected_value, user_profile):
    MembershipFactory(profile=user_profile, type=membership_type)
    assert user_profile.is_privileged() == expected_value
