from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import EventManager
from .querysets import EventQuerySet
from ..common.models import OwnedModel, TimeStampedModel
from ..common.utils import CustomEnum


class EventCategoryChoices(CustomEnum):
    EXAM = _('Exam')
    MID_TERM_EXAM = _('Mid term exam')
    PROJECT = _('Project')
    OTHER = _('Other')


class Event(TimeStampedModel, OwnedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=EventCategoryChoices.choices())
    due_date = models.DateTimeField()

    field_age_group = models.ForeignKey(
        'subject.FieldOfStudyOfAgeGroup', on_delete=models.PROTECT
    )
    subject_group = models.ForeignKey(
        'subject.SubjectOfAgeGroup', blank=True, null=True, on_delete=models.PROTECT
    )

    objects = EventManager.from_queryset(EventQuerySet)()

    def __str__(self) -> str:
        return self.name
