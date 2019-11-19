from rest_framework import viewsets

from lecturers.models import Lecturer
from lecturers.serializers import LecturerListSerializer


class LecturerViewSet(viewsets.ModelViewSet):
    serializer_class = LecturerListSerializer
    queryset = Lecturer.objects.all()
