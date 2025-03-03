from rest_framework import serializers
from main.apps.dashboard.models.construction_installation_work import (
    ConstructionFile,  
    Section
)



class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = (
            'id',
            'object',
            'title'
        )


class ConstructionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionFile
        fields = (
            'id',
            'section',
            'title',
            'full_name',
            'date',
            'file_code',
            'file'
        )

