from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OwnedModel(models.Model):
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='%(class)s_created')
    modified_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE,
                                    blank=True, null=True, related_name='%(class)s_modified')

    class Meta:
        abstract = True
