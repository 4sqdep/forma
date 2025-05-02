from django.db import models
from main.apps.account.models.user import User
from main.apps.common.models import BaseModel, BaseMeta
from main.apps.object_passport.models.object import Object





class Role(BaseModel):
    employee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Foydalanuvchi"
    )
    object = models.ManyToManyField(Object, verbose_name="Related Object", null=True, blank=True)
    has_construction_work = models.BooleanField(default=False)
    has_project_file = models.BooleanField(default=False)
    has_equipment = models.BooleanField(default=False)
    has_contract = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta(BaseMeta):
        db_table = "role"
        verbose_name = "Role"
        verbose_name_plural = "Roles"

