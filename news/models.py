from django.db import models

from common.models import TimeStampedModel


class News(TimeStampedModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    subject_group = models.ForeignKey('subject.SubjectOfAgeGroup', on_delete=models.PROTECT, related_name='news')

    class Meta:
        verbose_name = 'news'
        verbose_name_plural = 'news'
