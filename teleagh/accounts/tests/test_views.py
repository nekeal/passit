import pytest
from django.urls import reverse
from rest_framework.test import force_authenticate

from ..factories import MembershipFactory
from ..models import Membership
from ..views import CustomUserViewSet


@pytest.fixture
def custom_user_list_view():
    return CustomUserViewSet.as_view({'put': 'set_default_field_age_group', 'post': 'create'})


class TestCustomUserViewSet:

    def test_set_default_field_age_group_action(self, student1, api_rf, custom_user_list_view):
        default_membership = student1.memberships.get()

        non_default_membership: Membership = MembershipFactory(profile=student1, is_default=False)
        request = api_rf.put(reverse('accounts:users-set-default-field-age-group'),
                             data={'field_age_group': non_default_membership.field_age_group_id})
        force_authenticate(request, student1.user)
        custom_user_list_view(request)
        non_default_membership.refresh_from_db()
        default_membership.refresh_from_db()
        assert non_default_membership.is_default
        assert not default_membership.is_default
