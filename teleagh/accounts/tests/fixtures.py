import pytest

from ..factories import UserProfileFactory, MembershipFactory, UserFactory


@pytest.fixture
def user1(db):
    return UserFactory(username='student1')


@pytest.fixture
def user2(db):
    return UserFactory(username='student2')


@pytest.fixture
def user_profile1(db):
    return UserProfileFactory(user__username='student1')


@pytest.fixture
def user_profile2(db):
    return UserProfileFactory(user__username='student2')


@pytest.fixture
def user_profile_with_membership(user_profile1, field_age_group):
    MembershipFactory(profile=user_profile1, field_age_group=field_age_group)
    return user_profile1
