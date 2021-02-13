from django.db.models import QuerySet

from ..accounts.models import UserProfile


class FileQuerySet(QuerySet):  # type: ignore

    def filter_by_profile(self, profile: 'UserProfile'):
        return self.filter(created_by=profile)
