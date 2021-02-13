from typing import TYPE_CHECKING

from django.db.models import QuerySet, F

from passit.accounts.models import Membership, UserProfile

if TYPE_CHECKING:
    from passit.subject.models import FieldOfStudyOfAgeGroup

# TODO: move this to models.py


class FieldOfStudyQuerySet(QuerySet):  # type: ignore
    def filter_by_profile(self, profile: 'UserProfile'):
        from passit.subject.models import FieldOfStudyOfAgeGroup

        return self.filter(
            field_age_groups__in=FieldOfStudyOfAgeGroup.objects.filter_by_profile(
                profile
            )
        )


class FieldOfStudyOfAgeGroupQuerySet(QuerySet):  # type: ignore
    def filter_by_profile(
        self, profile: 'UserProfile'
    ) -> 'QuerySet[FieldOfStudyOfAgeGroup]':
        field_age_groups_ids = Membership.objects.filter(profile=profile).values(
            'field_age_group'
        )
        return self.filter(id__in=field_age_groups_ids)


class SubjectQuerySet(QuerySet):  # type: ignore
    def filter_by_profile(
        self, profile: 'UserProfile'
    ) -> 'QuerySet[FieldOfStudyOfAgeGroup]':
        field_of_study_ids = Membership.objects.filter(profile=profile).values(
            'field_age_group__field_of_study'
        )
        return self.filter(field_of_study_id__in=field_of_study_ids)


class ResourceQuerySet(QuerySet):  # type: ignore
    def filter_by_profile(
        self, profile: 'UserProfile'
    ) -> 'QuerySet[FieldOfStudyOfAgeGroup]':
        return self.filter(
            subject__field_of_study__field_age_groups__memberships__profile=profile
        )


class SubjectOfAgeGroupQuerySet(QuerySet):  # type: ignore
    def filter_by_profile(self, profile: 'UserProfile'):
        field_age_groups_ids = Membership.objects.filter(profile=profile).values(
            'field_age_group'
        )
        return self.filter(field_age_group_id__in=field_age_groups_ids)

    def add_subject_name(self):
        return self.annotate(subject_name=F('subject__name'))
