from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsRepresentativeOrModeratorOrReadOnly(BasePermission):

    def has_permission(self, request, view) -> bool:
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.profile.is_representative_or_moderator()
        )
