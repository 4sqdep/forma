from main.apps.checklist.serializers import CheckListSerializer
from rest_framework import serializers 
from .models import Contract
from django.utils.translation import gettext_lazy as _



class ContractCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = (
            'checklist',
            'subject_of_contract',
            'contract_amount',
            'date'
        )

 

class ContractListSerializer(serializers.ModelSerializer):
    checklist = CheckListSerializer()
    class Meta:
        model = Contract
        fields = (
            'id',
            'checklist',
            'subject_of_contract',
            'contract_amount',
            'date'
        )

