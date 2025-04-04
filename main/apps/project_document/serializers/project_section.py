from rest_framework import serializers
from main.apps.project_document.models.project_section import ProjectSection




class ProjectSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSection
        fields = (
            'id', 
            'project_document_type',
            'name'
        )

