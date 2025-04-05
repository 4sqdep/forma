from rest_framework import serializers
from main.apps.project_document.models.project_document_type import ProjectDocumentType
from main.apps.project_document.models.project_file import ProjectDocumentFile
from main.apps.project_document.models.project_fund import ConstructionTask
from main.apps.project_document.models.project_section import ProjectSection



class ProjectDocumentTypeSerializer(serializers.ModelSerializer):
    document_file_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ProjectDocumentType
        fields = (
            'id', 
            'object',
            'name',
            'is_forma',
            'is_section',
            'is_file',
            'document_file_name'
        )
    
    def get_document_file_name(self, obj):
        if obj.is_file:
            construction_installation_files = ProjectDocumentFile.objects.filter(project_document_type=obj)[:4]
            file_name_list = [document_file.name for document_file in construction_installation_files]
            return file_name_list if file_name_list else []  
        if obj.is_forma:
            construction_task = ConstructionTask.objects.filter(project_document_type=obj)[:4]
            construction_task_list = [project_name.title for project_name in construction_task]
            return construction_task_list if construction_task_list else [] 
        if obj.is_section:
            project_section = ProjectSection.objects.filter(project_document_type=obj)[:4]
            section_name_list = [project_name.name for project_name in project_section]
            return section_name_list if section_name_list else [] 
        return []



class ProjectDocumentTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocumentType
        fields = (
            'id',
            'object',
            'name', 
            'is_forma',
            'is_section', 
            'is_file'
        )