from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from ..accounts.models import UserProfile


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OwnedModel(models.Model):
    created_by = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='%(class)s_created',
    )
    modified_by = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='%(class)s_modified',
    )

    class Meta:
        abstract = True

    def is_owner(self, profile: 'UserProfile') -> bool:
        return profile == self.created_by
