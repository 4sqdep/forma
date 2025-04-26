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
        request = self.context.get('request')
        
        if obj.file and hasattr(obj.file, 'url'):
            file_url = obj.file.url  # example: /media/document_files/yourfile.pdf
            if request is not None:
                # Full absolute URL
                return request.build_absolute_uri(file_url)
            else:
                # fallback if request is not available
                return file_url
        return None
