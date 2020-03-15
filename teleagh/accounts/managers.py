from typing import TYPE_CHECKING

from django.contrib.auth.models import UserManager
from django.db.models import Manager, QuerySet

from .querysets import UserProfileQuerySet, CustomUserQuerySet, MembershipQuerySet

if TYPE_CHECKING:
    from .models import UserProfile, Membership


class CustomUserManager(UserManager.from_queryset(CustomUserQuerySet)):  # type: ignore
    pass


class UserProfileManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[UserProfile]':
        return UserProfileQuerySet(self.model, self._db)  # type: ignore


class MembershipManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[Membership]':
        return MembershipQuerySet(self.model, self._db)  # type: ignore

    def filter_by_profile(self, profile: 'UserProfile') -> 'QuerySet[Membership]':
        return self.get_queryset().filter(profile=profile)

    def get_default_by_profile(self, profile: 'UserProfile') -> 'Membership':
        return self.get_queryset().get(profile=profile, is_default=True)
