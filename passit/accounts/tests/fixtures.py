import pytest

from ..factories import MembershipFactory, UserFactory, UserProfileFactory
from ..models import MembershipTypeChoices, UserProfile


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
def student1(user_profile1, field_age_group):
    MembershipFactory(
        profile=user_profile1,
        field_age_group=field_age_group,
        is_default=True,
        type=MembershipTypeChoices.NORMAL,
    )
    return user_profile1


@pytest.fixture
def student2(user_profile2, field_age_group):
    MembershipFactory(
        profile=user_profile2,
        field_age_group=field_age_group,
        is_default=True,
        type=MembershipTypeChoices.NORMAL,
    )
    return user_profile2


@pytest.fixture
def representative_profile(field_age_group):
    profile = UserProfileFactory(user__username='representative1')
    MembershipFactory(
        profile=profile,
        field_age_group=field_age_group,
        is_default=True,
        type=MembershipTypeChoices.REPRESENTATIVE,
    )
    return profile
