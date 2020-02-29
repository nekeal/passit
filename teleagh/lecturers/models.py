from django.db import models

from teleagh.lecturers.managers import LecturerManager, LecturerOfSubjectManager
from teleagh.lecturers.querysets import LecturerQuerySet, LecturerOfSubjectQuerySet


class Lecturer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=20, blank=True)

    objects = LecturerManager.from_queryset(LecturerQuerySet)()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class LecturerOfSubject(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    subject_group = models.ForeignKey('subject.SubjectOfAgeGroup', on_delete=models.CASCADE,
                                      related_name='subject_groups')

    objects = LecturerOfSubjectManager.from_queryset(LecturerOfSubjectQuerySet)()

    def __str__(self) -> str:
        return f'{self.lecturer} {self.subject_group}'
