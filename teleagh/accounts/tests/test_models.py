from ..factories import MembershipFactory
from ..models import Membership


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
