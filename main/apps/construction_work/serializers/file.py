from rest_framework import serializers
from main.apps.construction_work.models.file import ConstructionInstallationFile





class ConstructionInstallationFileSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y",  input_formats=["%Y-%m-%d"], required=False)
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