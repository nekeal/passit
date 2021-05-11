import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..common.models import OwnedModel, TimeStampedModel
from ..common.utils import CustomEnum
from ..lecturers.models import Lecturer, LecturerOfSubjectOfAgeGroup
from .managers import (
    FieldOfStudyManager,
    FieldOfStudyOfAgeGroupManager,
    ResourceManager,
    SubjectManager,
    SubjectOfAgeGroupManager,
)
from .querysets import (
    FieldOfStudyOfAgeGroupQuerySet,
    FieldOfStudyQuerySet,
    ResourceQuerySet,
    SubjectOfAgeGroupQuerySet,
    SubjectQuerySet,
)


def year_validator(value):
    max_year = datetime.datetime.now().year
    if value < 2018 or value > max_year:
        raise ValidationError(
            f"{value} year is not valid. Provide value" f"between 2018 and {max_year}"
        )


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True, help_text="Slug which identifies field of study in syllabus"
    )

    objects = FieldOfStudyManager.from_queryset(FieldOfStudyQuerySet)()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Field of study"
        verbose_name_plural = "Fields of study"


class FieldOfStudyOfAgeGroup(models.Model):
    field_of_study = models.ForeignKey(
        "FieldOfStudy", on_delete=models.PROTECT, related_name="field_age_groups"
    )
    students_start_year = models.PositiveIntegerField(
        validators=[
            year_validator,
        ]
    )

    objects = FieldOfStudyOfAgeGroupManager.from_queryset(
        FieldOfStudyOfAgeGroupQuerySet
    )()

    def __str__(self):
        return f"{self.field_of_study} {self.students_start_year}"

    class Meta:
        verbose_name = "Field of study (age group)"
        verbose_name_plural = "Fields of study (age group)"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    semester = models.IntegerField()
    general_description = models.TextField()
    module_code = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=100)
    field_of_study = models.ForeignKey(
        "FieldOfStudy", on_delete=models.PROTECT, related_name="subjects"
    )

    objects = SubjectManager.from_queryset(SubjectQuerySet)()

    def __str__(self) -> str:
        return f"{self.name}"


class ResourceCategoryChoices(CustomEnum):
    LECTURE = _("Lecture")
    EXAM = _("Exam")
    MID_TERM_EXAM = _("Mid term exam")
    OTHER = _("Other")


class Resource(TimeStampedModel, OwnedModel):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    image = models.ImageField(blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=50, choices=ResourceCategoryChoices.choices()
    )
    subject = models.ForeignKey(
        "Subject", on_delete=models.CASCADE, related_name="resources"
    )

    objects = ResourceManager.from_queryset(ResourceQuerySet)()

    def __str__(self) -> str:
        return f"{self.name} - {self.subject}"


class SubjectOfAgeGroup(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="subjects"
    )
    description = models.TextField(blank=True)

    field_age_group = models.ForeignKey(
        "FieldOfStudyOfAgeGroup",
        on_delete=models.PROTECT,
        related_name="subject_groups",
    )
    lecturers = models.ManyToManyField(
        Lecturer, through=LecturerOfSubjectOfAgeGroup, related_name="subject_groups"
    )

    objects = SubjectOfAgeGroupManager.from_queryset(SubjectOfAgeGroupQuerySet)()

    def __str__(self) -> str:
        return f"{self.subject} {self.field_age_group}"

    class Meta:
        verbose_name = "Subject (age group)"
        verbose_name_plural = "Subjects (age group)"

    @property
    def students_start_year(self):
        if hasattr(self, "start_year"):
            return self.start_year  # type: ignore
        return self.field_age_group.students_start_year


class Exam(models.Model):
    subject_group = models.ForeignKey(
        SubjectOfAgeGroup, on_delete=models.CASCADE, related_name="exams"
    )
    starts_at = models.DateTimeField()
    place = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.subject_group} {self.starts_at}"
