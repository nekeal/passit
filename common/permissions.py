from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPrivilegedOrReadOnly(BasePermission):

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user.is_authenticated
            and (
                request.method in SAFE_METHODS
                or request.user
                and request.user.profile.is_privileged()
            ))
