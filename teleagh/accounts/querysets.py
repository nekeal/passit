from django.db.models import QuerySet


class CustomUserQuerySet(QuerySet):  # type: ignore
    pass


class UserProfileQuerySet(QuerySet):  # type: ignore
    pass


class MembershipQuerySet(QuerySet):  # type: ignore
    pass
