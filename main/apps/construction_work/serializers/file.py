from rest_framework import serializers
from main.apps.construction_work.models.file import ConstructionInstallationFile





class ConstructionInstallationFileSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y",  input_formats=["%Y-%m-%d"], required=False)
    file_name = serializers.SerializerMethodField(required=False)
    code = serializers.SerializerMethodField()

    class Meta:
        model = ConstructionInstallationFile
        fields = (
            "id", 
            "section", 
            "title", 
            "date", 
            "file_code", 
            "file", 
            'file_name',
            'code'
        )
    
    def get_file_name(self, obj):
        from urllib.parse import unquote
        
        if obj.file:
            file_url = obj.file.url
            filename_encoded = file_url.split("/")[-1]
            filename = unquote(filename_encoded)
            return filename.replace(" ", "_")
        return None
    
    def get_code(self, obj):
        try:
            return obj.section.object.code
        except AttributeError:
            return None