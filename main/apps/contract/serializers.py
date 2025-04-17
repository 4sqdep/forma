from rest_framework import serializers
from main.apps.contract.models import ContractSection, ContractFile


class ContractSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractSection
        fields = ['id', 'object', 'title']



class ContractSectionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractFile
        fields = ['id', 'section', 'title', 'date', 'file_code', 'file']