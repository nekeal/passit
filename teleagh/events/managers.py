from typing import TYPE_CHECKING

from django.db.models import Manager, QuerySet

from .querysets import EventQuerySet
from ..accounts.models import UserProfile, Membership

if TYPE_CHECKING:
    from .models import Event


class EventManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[Event]':
        return EventQuerySet(self.model, using=self._db)  # type: ignore

    def get_by_profile(self, profile: UserProfile) -> 'QuerySet[Event]':
        member_of = Membership.objects.filter_by_profile(profile).values_list('field_age_group_id')
        return self.get_queryset().filter(field_age_group_id__in=member_of)
