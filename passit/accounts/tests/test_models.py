import pytest

from ..factories import MembershipFactory, UserFactory, UserProfileFactory
from ..models import Membership, MembershipTypeChoices


class TestUserProfile:
    def test_str_method(self):
        profile = UserProfileFactory.build()
        assert str(profile) == str(profile.user)

    @pytest.mark.parametrize("create_user", (True, False))
    @pytest.mark.django_db
    def test_get_display_name(self, create_user):
        profile = UserProfileFactory.build(user=None)
        if create_user:
            profile.user = UserFactory()
            profile.user_id = 1
            assert (
                profile.get_name()
                == f"{profile.user.first_name} {profile.user.last_name}"
            )
        else:
            assert profile.get_name() == "Anonymous"

    def test_set_default_field_age_group_with_other_field_age_group(
        self, user_profile1, django_assert_num_queries
    ):
        default_membership = MembershipFactory(profile=user_profile1, is_default=True)
        other_membership = MembershipFactory(profile=user_profile1, is_default=False)
        with django_assert_num_queries(4):
            result = user_profile1.set_default_field_age_group(
                other_membership.field_age_group
            )
        assert result == other_membership
        default_membership.refresh_from_db()
        assert default_membership.is_default is False

    def test_set_default_field_age_group_with_same_field_age_group(
        self, user_profile1, django_assert_num_queries
    ):
        default_membership = MembershipFactory(profile=user_profile1, is_default=True)
        with django_assert_num_queries(2):
            result = user_profile1.set_default_field_age_group(
                default_membership.field_age_group
            )
        assert result == default_membership

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ("membership_type", "expected_privileged"),
        (
            (MembershipTypeChoices.NORMAL, False),
            (MembershipTypeChoices.REPRESENTATIVE, True),
            (MembershipTypeChoices.MODERATOR, True),
        ),
    )
    def test_profile_is_privileged(
        self, membership_type, expected_privileged, user_profile1
    ):
        MembershipFactory(profile=user_profile1, type=membership_type)
        assert user_profile1.is_privileged() is expected_privileged


class TestMembershipTypeChoices:
    def test_privileged_membership_types(self):
        assert MembershipTypeChoices.privileged_membership_types() == [
            MembershipTypeChoices.REPRESENTATIVE,
            MembershipTypeChoices.MODERATOR,
        ]


class TestMembershipQuerySet:
    def test_filter_by_profile_method(self, user_profile1, user_profile2):
        expected = MembershipFactory.create_batch(2, profile=user_profile1)
        MembershipFactory(profile=user_profile2)
        assert set(Membership.objects.filter_by_profile(user_profile1)) == set(expected)

    def test_get_default_by_profile(self, user_profile1, user_profile2):
        expected = MembershipFactory(profile=user_profile1, is_default=True)
        MembershipFactory(profile=user_profile1, is_default=False)
        MembershipFactory(profile=user_profile2, is_default=True)
        assert Membership.objects.get_default_by_profile(user_profile1) == expected


class TestCustomUserManager:
    def test_create_student_without(self, field_age_group):
        pass
