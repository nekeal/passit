from django.contrib import admin

# Register your models here.
from .models import Lecturer, LecturerOfSubjectOfAgeGroup

admin.site.register(Lecturer)
admin.site.register(LecturerOfSubjectOfAgeGroup)
