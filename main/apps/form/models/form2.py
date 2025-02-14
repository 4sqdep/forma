from django.db import models
from main.apps.common.models import BaseMeta, BaseModel
from django.utils.translation import gettext_lazy as _
from main.apps.common.utils import upload_file





class Template(BaseModel):
    file = models.FileField(upload_to=upload_file('templates/'), null=True)
    is_active = models.BooleanField(default=True)

    class Meta(BaseMeta):
        db_table = "template"
        verbose_name = "Template"
        verbose_name_plural = "Templates"



class Form2(BaseModel):
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(null=True, blank=True)
    attached_document = models.FileField(upload_to=upload_file('attached_document/'), null=True, blank=True)
    is_delivered_to_recipient = models.BooleanField(default=False)
    is_response_required = models.BooleanField(default=False)

    class Meta(BaseMeta):
        db_table = "form2"
        verbose_name = "Form2"
        verbose_name_plural = "Form2s"

    


    