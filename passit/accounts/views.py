from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from passit.accounts.serializers import (
    DefaultFieldOfAgeGroupSerializer,
    MembershipSerializer,
)


class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == 'set_default_field_age_group':
            return DefaultFieldOfAgeGroupSerializer
        return super().get_serializer_class()

    @action(
        methods=['put'], detail=False, url_path='set_default_fag'
    )  # TODO: add permission
    def set_default_field_age_group(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data, instance=request.user.profile)
        serializer.is_valid(raise_exception=True)
        new_default = serializer.update(request.user.profile, serializer.validated_data)
        return Response(
            MembershipSerializer(new_default).data, status=status.HTTP_200_OK
        )
