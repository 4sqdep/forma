from rest_framework import serializers
from main.apps.construction_work.models.file import ConstructionInstallationFile





class ConstructionInstallationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionInstallationFile
        fields = (
            "id", 
            "section", 
            "title", 
            "date", 
            "file_code", 
            "file", 
        )