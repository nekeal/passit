from django.db.models import QuerySet, Case, When, BooleanField
from django.db.models.expressions import Value

from teleagh.accounts.models import UserProfile


class NewsQuerySet(QuerySet):  # type: ignore

    def annotate_is_owner(self, profile: 'UserProfile'):
        return self.annotate(is_news_owner=Case(
            When(
                created_by_id=profile.id,
                then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ))
