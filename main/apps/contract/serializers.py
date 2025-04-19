from rest_framework import serializers
from main.apps.contract.models import ContractSection, ContractFile


class ContractSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractSection
        fields = ['id', 'object', 'title']



class ContractSectionFileSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y", input_formats=["%Y-%m-%d"], required=False)
    class Meta:
        model = ContractFile
        fields = ['id', 'section', 'title', 'date', 'file_code', 'file']