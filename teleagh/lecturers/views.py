from rest_framework import viewsets

from .models import Lecturer
from .serializers import LecturerListSerializer


class LecturerViewSet(viewsets.ModelViewSet):
    serializer_class = LecturerListSerializer
    queryset = Lecturer.objects.all()
