import pytest

from accounts.factories import UserProfileFactory, MembershipFactory, UserFactory
from accounts.models import UserProfile


@pytest.fixture
def user(db):
    return UserFactory(username='student')


@pytest.fixture
def user_profile(db) -> 'UserProfile':
    return UserProfileFactory(user__username='student')


@pytest.fixture
def user_profile_with_membership(user_profile, field_age_group):
    MembershipFactory(profile=user_profile, field_age_group=field_age_group)
    return user_profile
