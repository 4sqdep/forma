from rest_framework import serializers
from main.apps.project_document.models.project_file import ProjectDocumentFile





class FileSerializer(serializers.ModelSerializer):
    calendar = serializers.DateField(format="%d-%m-%Y",  input_formats=["%Y-%m-%d"], required=False)
    class Meta:
        model = ProjectDocumentFile
        fields = (
            'id',
            'project_document_type',
            'project_section',
            'name',
            'full_name',
            'calendar',
            'file_code',
            'file'
        )