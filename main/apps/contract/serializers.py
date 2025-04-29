from rest_framework import serializers
from main.apps.contract.models import ContractSection, ContractFile







class ContractSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractSection
        fields = ['id', 'object', 'title']



class ContractSectionFileSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y", input_formats=["%Y-%m-%d"], required=False)
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = ContractFile
        fields = ['id', 'section', 'title', 'date', 'file_code', 'file', 'file_name']

    
    def get_file_name(self, obj):
        from urllib.parse import unquote
        
        if obj.file:
            file_url = obj.file.url
            filename_encoded = file_url.split("/")[-1]
            filename = unquote(filename_encoded)
            return filename.replace(" ", "_")
        return None