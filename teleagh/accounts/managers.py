from typing import TYPE_CHECKING, Optional

from django.contrib.auth.models import UserManager
from django.db.models import Manager, QuerySet

from .querysets import UserProfileQuerySet, CustomUserQuerySet, MembershipQuerySet

if TYPE_CHECKING:
    from .models import UserProfile, Membership, FieldOfStudyOfAgeGroup


class CustomUserManager(UserManager.from_queryset(CustomUserQuerySet)):  # type: ignore
    def get_queryset(self):
        return super().get_queryset().select_related('profile')

    def create_student(self, username: str, field_age_group: 'FieldOfStudyOfAgeGroup', type: int, first_name, last_name,
                       email: Optional[str] = None, password: Optional[str] = None):
        from .models import UserProfile, Membership
        user = super(CustomUserManager, self).create_user(username, email, password)
        profile = UserProfile.objects.create(user=user)
        Membership.objects.create(profile=profile, field_age_group=field_age_group)
        return user


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
