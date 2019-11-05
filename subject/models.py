import datetime

from django.core.exceptions import ValidationError
from django.db import models

from common.models import TimeStampedModel, OwnedModel
from lecturers.models import LecturerOfSubject, Lecturer


def year_validator(value):
    max_year = datetime.datetime.now().year
    if value < 2018 or value > max_year:
        raise ValidationError(f"{value} year is not valid. Provide value"
                              f"between 2018 and {max_year}")


class Resource(TimeStampedModel, OwnedModel):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    image = models.ImageField(blank=True)
    description = models.TextField(blank=True)

    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='resources')

    def __str__(self) -> str:
        return f'{self.name} - {self.subject}'


class FieldOfStudies(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=50)
    semester = models.IntegerField()
    general_description = models.TextField()
    field_of_studies = models.ForeignKey('FieldOfStudies', on_delete=models.PROTECT, related_name='subjects')

    def __str__(self) -> str:
        return f'{self.name}'


class SubjectOfAgeGroup(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subjects')
    students_start_year = models.PositiveIntegerField(validators=[year_validator, ])
    description = models.TextField(blank=True)
    lecturers = models.ManyToManyField(Lecturer, through=LecturerOfSubject, related_name='lecturer_age_groups')

    def __str__(self) -> str:
        return f"{self.subject} {self.students_start_year}"


class Exam(models.Model):
    subject_group = models.ForeignKey(SubjectOfAgeGroup, on_delete=models.CASCADE, related_name='exams')
    starts_at = models.DateTimeField()
    place = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.subject_group}'
