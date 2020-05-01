from typing import Dict

from django.conf import settings
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import ThumbnailFile

from .managers import FileManager
from .querysets import FileQuerySet
from ..common.models import OwnedModel


class File(OwnedModel):
    name = models.CharField(max_length=100, blank=True)
    other = models.FileField('files/', blank=True, null=True)
    image = ThumbnailerImageField('images/', blank=True, null=True)

    objects = FileManager.from_queryset(FileQuerySet)()

    def get_thumbnails(self) -> Dict[str, ThumbnailFile]:
        thumbnail_names = settings.THUMBNAIL_ALIASES[''].keys()
        return {name: self.image[name] for name in thumbnail_names}
