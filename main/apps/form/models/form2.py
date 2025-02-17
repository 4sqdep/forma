from django.db import models
from main.apps.common.models import BaseMeta, BaseModel, Template
from django.utils.translation import gettext_lazy as _




class Form2(BaseModel):
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(null=True, blank=True)
    attached_document = models.FileField(upload_to='attached_document/', null=True, blank=True)
    is_delivered_to_recipient = models.BooleanField(default=False)
    is_response_required = models.BooleanField(default=False)
    without_qr_code = models.BooleanField(default=False)

    class Meta(BaseMeta):
        db_table = "form2"
        verbose_name = "Form2"
        verbose_name_plural = "Form2"

    


    