from enum import IntEnum
from typing import Tuple, List

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

from teleagh.accounts.managers import CustomUserManager, UserProfileManager, MembershipManager
from teleagh.accounts.querysets import UserProfileQuerySet, MembershipQuerySet


class CustomUser(AbstractUser):

    objects = CustomUserManager()


class UserProfile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='profile')
    field_age_groups = models.ManyToManyField('subject.FieldOfStudyOfAgeGroup', blank=True,
                                              through='Membership', related_name='students')

    objects = UserProfileManager.from_queryset(UserProfileQuerySet)()

    def __str__(self) -> str:
        return f'{self.user}'

    def get_name(self) -> str:
        if self.user_id:
            return f'{self.user.first_name} {self.user.last_name}'
        return 'Anonymous'

    def is_privileged(self) -> bool:
        return Membership.objects.filter(Q(profile=self)
                                         & (Q(type__in=MembershipTypeChoices.privileged_membership_types()))).exists()


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


class Membership(models.Model):
    profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='memberships')
    field_age_group = models.ForeignKey('subject.FieldOfStudyOfAgeGroup', on_delete=models.CASCADE,
                                        related_name='memberships')
    type = models.PositiveSmallIntegerField(default=MembershipTypeChoices.NORMAL,
                                            choices=MembershipTypeChoices.choices())

    objects = MembershipManager.from_queryset(MembershipQuerySet)()
