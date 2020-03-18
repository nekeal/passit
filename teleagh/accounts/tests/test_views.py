
# --- CustomUserViewSet ---
import pytest
from django.urls import reverse
from rest_framework.test import force_authenticate

from ..factories import MembershipFactory
from ..models import Membership
from ..views import CustomUserViewSet


@pytest.fixture
def custom_user_list_view():
    return CustomUserViewSet.as_view({'put': 'set_default_field_age_group', 'post': 'create'})


def test_set_default_field_age_group_action(user_profile1_with_membership, api_rf, custom_user_list_view):
    default_membership = user_profile1_with_membership.memberships.get()

    non_default_membership: Membership = MembershipFactory(profile=user_profile1_with_membership, is_default=False)
    request = api_rf.put(reverse('accounts:users-set-default-field-age-group'),
                         data={'field_age_group': non_default_membership.field_age_group_id})
    force_authenticate(request, user_profile1_with_membership.user)
    custom_user_list_view(request)
    non_default_membership.refresh_from_db()
    default_membership.refresh_from_db()
    assert non_default_membership.is_default
    assert not default_membership.is_default
