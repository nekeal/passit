from enum import IntEnum
from typing import TYPE_CHECKING, List, Optional, Tuple

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Manager, Q, QuerySet

if TYPE_CHECKING:
    from ..subject.models import FieldOfStudyOfAgeGroup


class MembershipTypeChoices(IntEnum):
    REPRESENTATIVE = 1
    MODERATOR = 2
    NORMAL = 3

    @classmethod
    def choices(cls) -> List[Tuple[int, str]]:
        return [(key.value, key.name) for key in cls]

    @classmethod
    def privileged_membership_types(cls) -> List[int]:
        return [cls.REPRESENTATIVE, cls.MODERATOR]


class CustomUserQuerySet(QuerySet):  # type: ignore
    pass


class CustomUserManager(UserManager.from_queryset(CustomUserQuerySet)):  # type: ignore
    def get_queryset(self):
        return super().get_queryset().select_related('profile')

    def create_student(
        self,
        username: str,
        field_age_group: 'FieldOfStudyOfAgeGroup',
        first_name,
        last_name,
        membership_type: int = MembershipTypeChoices.NORMAL,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ):
        from .models import Membership, UserProfile

        user = super(CustomUserManager, self).create_user(username, email, password)
        profile = UserProfile.objects.create(user=user)
        Membership.objects.create(
            profile=profile, field_age_group=field_age_group, type=membership_type
        )
        return user


class CustomUser(AbstractUser):

    objects = CustomUserManager()


class UserProfileQuerySet(QuerySet):  # type: ignore
    pass


class UserProfileManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[UserProfile]':
        return UserProfileQuerySet(self.model, self._db)  # type: ignore


class UserProfile(models.Model):
    user = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE, related_name='profile'
    )
    field_age_groups = models.ManyToManyField(
        'subject.FieldOfStudyOfAgeGroup',
        blank=True,
        through='Membership',
        related_name='students',
    )

    objects = UserProfileManager.from_queryset(UserProfileQuerySet)()

    def __str__(self) -> str:
        return f'{self.user}'

    def get_name(self) -> str:
        if self.user_id:
            return f'{self.user.first_name} {self.user.last_name}'
        return 'Anonymous'

    def is_privileged(self) -> bool:
        return Membership.objects.filter(
            Q(profile=self)
            & (Q(type__in=MembershipTypeChoices.privileged_membership_types()))
        ).exists()

    def set_default_field_age_group(
        self, field_age_group: 'FieldOfStudyOfAgeGroup'
    ) -> 'Membership':
        current_default = Membership.objects.get_default_by_profile(self)
        new_default = Membership.objects.filter_by_profile(self).get(
            field_age_group=field_age_group
        )
        if new_default == current_default:
            return current_default
        Membership.objects.filter_by_profile(self).update(is_default=False)
        new_default.is_default = True
        new_default.save()
        return new_default


class MembershipQuerySet(QuerySet):  # type: ignore
    pass


class MembershipManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[Membership]':
        return MembershipQuerySet(self.model, self._db)  # type: ignore

    def filter_by_profile(self, profile: 'UserProfile') -> 'QuerySet[Membership]':
        return self.get_queryset().filter(profile=profile)

    def get_default_by_profile(self, profile: 'UserProfile') -> 'Membership':
        return self.get_queryset().get(profile=profile, is_default=True)


class Membership(models.Model):
    profile = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='memberships'
    )
    field_age_group = models.ForeignKey(
        'subject.FieldOfStudyOfAgeGroup',
        on_delete=models.CASCADE,
        related_name='memberships',
    )
    type = models.PositiveSmallIntegerField(
        default=MembershipTypeChoices.NORMAL, choices=MembershipTypeChoices.choices()
    )
    is_default = models.BooleanField(default=False)

    objects = MembershipManager.from_queryset(MembershipQuerySet)()

    class Meta:
        unique_together = ('profile', 'field_age_group')
