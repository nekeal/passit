from django.db import models

from ..common.models import TimeStampedModel

from .managers import NewsManager
from .querysets import NewsQuerySet


class News(TimeStampedModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    subject_group = models.ForeignKey('subject.SubjectOfAgeGroup', on_delete=models.PROTECT, related_name='news')
    field_age_group = models.ForeignKey('subject.FieldOfStudyOfAgeGroup', on_delete=models.PROTECT, related_name='news')

    objects = NewsManager.from_queryset(NewsQuerySet)()

    def __str__(self) -> str:
        return f'{self.subject_group}'

    class Meta:
        verbose_name = 'news'
        verbose_name_plural = 'news'
