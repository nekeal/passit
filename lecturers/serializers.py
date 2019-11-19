from rest_framework import serializers

from lecturers.models import Lecturer


class LecturerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecturer
        fields = ('id', 'first_name', 'last_name', 'title')
