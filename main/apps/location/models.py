from django.db import models
from ..common.models import BaseModel, BaseMeta


class Country(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta(BaseMeta):
        verbose_name = 'Country'
        verbose_name_plural = 'Countries' 

    def __str__(self):
        return self.name


class Region(BaseModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    class Meta(BaseMeta):
        verbose_name = 'Region'
        verbose_name_plural = 'Regions' 

    def __str__(self):
        return self.name


class District(BaseModel):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="districts")

    class Meta(BaseMeta):
        verbose_name = 'District'
        verbose_name_plural = 'Districts'
        unique_together = ('name', 'region') 

    def __str__(self):
        return f"{self.name} ({self.region.name})"


