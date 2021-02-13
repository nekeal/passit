from rest_framework import viewsets

from .models import File
from .serializers import FileSerializer
from ..common.permissions import IsStudent, IsOwner


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsStudent, IsOwner)

    def get_queryset(self):
        return File.objects.filter_by_profile(self.request.user.profile)
