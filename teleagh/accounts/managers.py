from typing import TYPE_CHECKING

from django.contrib.auth.models import UserManager
from django.db.models import Manager, QuerySet

from .querysets import UserProfileQuerySet, CustomUserQuerySet, MembershipQuerySet

if TYPE_CHECKING:
    from .models import CustomUser, UserProfile, Membership


class CustomUserManager(UserManager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[CustomUser]':
        return CustomUserQuerySet(self.model, self._db)  # type: ignore


class UserProfileManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[UserProfile]':
        return UserProfileQuerySet(self.model, self._db)  # type: ignore


class MembershipManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[Membership]':
        return MembershipQuerySet(self.model, self._db)  # type: ignore
