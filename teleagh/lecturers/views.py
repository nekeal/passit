from rest_framework import viewsets

from .models import Lecturer
from .serializers import LecturerBaseSerializer


class LecturerViewSet(viewsets.ModelViewSet):
    serializer_class = LecturerBaseSerializer
    queryset = Lecturer.objects.all()
