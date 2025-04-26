from rest_framework import serializers
from main.apps.project_document.models.project_file import ProjectDocumentFile





class FileCreateSerializer(serializers.ModelSerializer):
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

    


class FileSerializer(serializers.ModelSerializer):
    calendar = serializers.DateField(format="%d-%m-%Y",  input_formats=["%Y-%m-%d"], required=False)
    file = serializers.SerializerMethodField()

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
    
    def get_file(self, obj):
        from urllib.parse import unquote
        
        if obj.file:
            file_url = obj.file.url
            filename_encoded = file_url.split("/")[-1]
            filename = unquote(filename_encoded)
            return filename.replace(" ", "_")
        return None