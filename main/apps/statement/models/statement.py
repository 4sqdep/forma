from django.db import models
from main.apps.account.models import User
from main.apps.common.models import BaseMeta, BaseModel
from main.apps.location.models import Country, District, Region


# class StatusChoices(models.TextChoices):
#     NEW = 'new'
#     CANCEL = 'cancel'
#     COMPLETED = 'completed'


# class BaseClientStatement(BaseModel):
#     full_name = models.CharField(max_length=255, null=True, blank=True)
#     phone_number = models.CharField(max_length=255, null=True, blank=True)
#     region = models.ForeignKey(Region, on_delete=models.CASCADE)
#     district = models.ForeignKey(District, on_delete=models.CASCADE)
#     street = models.CharField(max_length=255, null=True, blank=True)
#     address = models.CharField(max_length=255, null=True, blank=True)
#     comment = models.TextField(null=True, blank=True)
#     status = models.CharField(
#         max_length=255,
#         choices=StatusChoices.choices,
#         default=StatusChoices.NEW  
#     )
    
#     class Meta:
#         abstract = True


# class CorporateClientStatement(BaseClientStatement):
#     inn = models.CharField(max_length=255, null=True, blank=True)
#     contract_number = models.CharField(max_length=255, null=True, blank=True)
#     email = models.EmailField(null=True, blank=True)
#     contact_full_name = models.CharField(max_length=255, null=True, blank=True)
#     contact_phone_number = models.CharField(max_length=255, null=True, blank=True)


# class IndividualClientStatement(BaseClientStatement):
#     pass 





class StatusChoices(models.TextChoices):
    NEW = 'new'
    COMPLETED = 'completed'
    CANCEL = 'cancel'


class ClientTypeChoices(models.TextChoices):
    CORPORATE = 'corporate'
    INDIVIDUAL = 'individual'


class Statement(BaseModel):
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    client_type = models.CharField(max_length=255, choices=ClientTypeChoices.choices)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    # country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    street = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=255,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW  
    )
    inn = models.CharField(max_length=255, null=True, blank=True)
    contract_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact_full_name = models.CharField(max_length=255, null=True, blank=True)
    contact_phone_number = models.CharField(max_length=255, null=True, blank=True)


    class Meta(BaseMeta):
        verbose_name = 'Statement'
        verbose_name_plural = 'Statements' 

    def __str__(self):
        return self.full_name