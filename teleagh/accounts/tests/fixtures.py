import pytest

from ..factories import UserProfileFactory, MembershipFactory, UserFactory
from ..models import UserProfile


@pytest.fixture
def user1(db):
    return UserFactory(username='student1')


@pytest.fixture
def user2(db):
    return UserFactory(username='student2')


@pytest.fixture
def user_profile1(db) -> UserProfile:
    return UserProfileFactory(user__username='student1')


@pytest.fixture
def user_profile2(db) -> UserProfile:
    return UserProfileFactory(user__username='student2')


@pytest.fixture
def user_profile1_with_membership(user_profile1, field_age_group):
    MembershipFactory(profile=user_profile1, field_age_group=field_age_group, is_default=True)
    return user_profile1

@pytest.fixture
def user_profile2_with_membership(user_profile2, field_age_group):
    MembershipFactory(profile=user_profile2, field_age_group=field_age_group, is_default=True)
    return user_profile2
