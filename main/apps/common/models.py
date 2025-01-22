import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='%(app_label)s_%(class)s_created_by'
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='%(app_label)s_%(class)s_deleted_by'
    )

    class Meta:
        abstract = True


class BaseMeta(object):
    ordering = ("-id",)