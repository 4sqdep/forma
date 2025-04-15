import os
from django.db import models
from django.utils.timezone import now
from main.apps.common.models import BaseModel, BaseMeta
from main.apps.object_passport.models.object import Object



class ContractSection(BaseModel):
    object = models.ForeignKey(Object, on_delete=models.SET_NULL, verbose_name="Obyekt", null=True, blank=True)
    title = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nomi")

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "contract_section"
        verbose_name = "Contract Section"
        verbose_name_plural = "Contract Sections"


def upload_contract_files(instance, filename):
    ext = os.path.splitext(filename)[1]
    original_name = os.path.splitext(filename)[0]
    timestamp = now().strftime("%Y_%m_%d")
    return f"contract_file/{original_name}_{timestamp}{ext}"


class ContractFile(BaseModel):
    section = models.ForeignKey(ContractSection, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    file_code = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=upload_contract_files, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta(BaseMeta):
        db_table = "contract_file"
        verbose_name = "Contract File"
        verbose_name_plural = "Contract Files"