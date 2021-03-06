from django.db import models

from ..common.models import OwnedModel, TimeStampedModel
from .managers import NewsManager
from .querysets import NewsQuerySet


class News(TimeStampedModel, OwnedModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    attachment = models.FileField(upload_to="attachments", blank=True)

    field_age_group = models.ForeignKey(
        "subject.FieldOfStudyOfAgeGroup",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="news",
    )
    subject_group = models.ForeignKey(
        "subject.SubjectOfAgeGroup",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="news",
    )

    objects = NewsManager.from_queryset(NewsQuerySet)()

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "news"
        verbose_name_plural = "news"
