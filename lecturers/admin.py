from django.contrib import admin

# Register your models here.
from lecturers.models import Lecturer, LecturerOfSubject

admin.site.register(Lecturer)
admin.site.register(LecturerOfSubject)
