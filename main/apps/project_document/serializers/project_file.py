from rest_framework import serializers
from main.apps.project_document.models.project_file import ProjectDocumentFile





class FileSerializer(serializers.ModelSerializer):
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