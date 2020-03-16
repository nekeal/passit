from typing import TYPE_CHECKING

from django.db.models import Manager, QuerySet, Q

from .querysets import EventQuerySet
from ..accounts.models import UserProfile, Membership

if TYPE_CHECKING:
    from .models import Event


class EventManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[Event]':
        return EventQuerySet(self.model, using=self._db)  # type: ignore

    def get_by_profile(self, profile: UserProfile) -> 'QuerySet[Event]':
        member_of = Membership.objects.filter(profile=profile).values('field_age_group_id')
        return self.get_queryset().filter(Q(subject_group__field_age_group_id__in=member_of))
