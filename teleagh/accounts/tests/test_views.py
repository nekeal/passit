import pytest

from ..factories import MembershipFactory
from ..models import Membership
from ..views import CustomUserViewSet
from ...common.utils import ResponseFactory


@pytest.fixture
def custom_user_list_view():
    return CustomUserViewSet.as_view({'put': 'set_default_field_age_group', 'post': 'create'})


class TestCustomUserViewSet:

    def test_set_default_field_age_group_action2(self, student1, api_rf, custom_user_list_view):
        default_membership = student1.memberships.get()
        url = '/api/auth/users/set_default_fag/'
        non_default_membership: Membership = MembershipFactory(profile=student1, is_default=False)

        ResponseFactory(url, data={'field_age_group': non_default_membership.field_age_group_id}, method='put',
                        user=student1.user).get()
        non_default_membership.refresh_from_db()
        default_membership.refresh_from_db()
        assert non_default_membership.is_default
        assert not default_membership.is_default
