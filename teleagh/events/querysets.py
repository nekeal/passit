from django.db.models import QuerySet

from teleagh.accounts.models import UserProfile
from teleagh.subject.models import FieldOfStudyOfAgeGroup


class EventQuerySet(QuerySet):  # type: ignore
    def filter_by_user_profile_default_field_age_group(self, user_profile: 'UserProfile'):
        return self.filter(field_age_group=FieldOfStudyOfAgeGroup.objects.get_default_by_profile(user_profile))
