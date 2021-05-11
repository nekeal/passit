from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsPrivilegedOrOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return bool(
            request.user.is_authenticated
            and (
                request.method in SAFE_METHODS
                or request.user
                and (
                    request.user.profile.is_privileged()
                    or hasattr(obj, "is_owner")
                    and obj.is_owner(request.user.profile)
                )
            )
        )
