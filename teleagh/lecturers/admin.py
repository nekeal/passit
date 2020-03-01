from django.contrib import admin

# Register your models here.
from .models import Lecturer, LecturerOfSubject

admin.site.register(Lecturer)
admin.site.register(LecturerOfSubject)
