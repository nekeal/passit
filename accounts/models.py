from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='profile')
    own_field_group = models.ForeignKey('subject.FieldOfStudyOfAgeGroup', on_delete=models.PROTECT,
                                        null=True, blank=True, related_name='representatives')
    field_groups = models.ManyToManyField('subject.FieldOfStudyOfAgeGroup', blank=True, through='Membership',
                                          related_name='students')


class Membership(models.Model):
    profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='memberships')
    field_group = models.ForeignKey('subject.FieldOfStudyOfAgeGroup', on_delete=models.CASCADE,
                                    related_name='memberships')
