from typing import TYPE_CHECKING

from django.db.models import Manager, QuerySet, Q, Subquery

from accounts.models import UserProfile, Membership

from .querysets import NewsQuerySet

if TYPE_CHECKING:
    from .models import News


class NewsManager(Manager):  # type: ignore
    def get_queryset(self) -> 'QuerySet[News]':
        return NewsQuerySet(self.model, using=self._db)  # type: ignore

    def get_by_profile(self, profile: UserProfile) -> 'QuerySet[News]':
        member_of = Membership.objects.filter(profile=profile).values('field_age_group_id')
        return self.get_queryset().filter(Q(subject_group__field_age_group_id__in=member_of))
