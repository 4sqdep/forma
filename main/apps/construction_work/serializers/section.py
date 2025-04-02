from rest_framework import serializers
from main.apps.construction_work.models.file import ConstructionInstallationFile
from main.apps.construction_work.models.fund import ConstructionInstallationProject
from main.apps.construction_work.models.section import ConstructionInstallationSection




class ConstructionInstallationSectionSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ConstructionInstallationSection
        fields = (
            'id',
            'object',
            'title',
            'is_forma',
            'is_file',
            'file_name'
        )

    def get_file_name(self, obj):
        if obj.is_file:
            construction_installation_files = ConstructionInstallationFile.objects.filter(section=obj)[:4]
            file_name_list = [document_file.title for document_file in construction_installation_files]
            return file_name_list if file_name_list else []  
        if obj.is_forma:
            construction_installation_project = ConstructionInstallationProject.objects.filter(section=obj)[:4]
            project_name_list = [project_name.title for project_name in construction_installation_project]
            return project_name_list if project_name_list else [] 
        return [] 
