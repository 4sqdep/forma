from main.apps.location.serializer import DistrictSerializer, RegionSerializer
from main.apps.statement.models.statement import Statement
from rest_framework import serializers 



class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = (
            'id',
            'guid',
            'employee',
            "client_type",
            'full_name',
            'phone_number',
            'region',
            'district',
            'street',
            'address',
            'comment',
            'status',
            'inn',
            'contract_number',
            'email',
            "contact_full_name",
            "contact_phone_number"
            
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.client_type == 'individual':
            data.pop('inn', None)
            data.pop('email', None)
            data.pop('contract_number', None)
            data.pop('contact_full_name', None)
            data.pop('contact_phone_number', None)
        return data


class StatementListSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    district = DistrictSerializer()
    class Meta:
        model = Statement
        fields = (
            'id',
            'guid',
            'employee',
            "client_type",
            'full_name',
            'phone_number',
            'region',
            'district',
            'street',
            'address',
            'comment',
            'status',
            'inn',
            'contract_number',
            'email',
            "contact_full_name",
            "contact_phone_number"
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.client_type == 'individual':
            data.pop('inn', None)
            data.pop('email', None)
            data.pop('contract_number', None)
            data.pop('contact_full_name', None)
            data.pop('contact_phone_number', None)
        return data
    


class StatementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = (
            'employee',
            'client_type',
            'full_name',
            'phone_number',
            'region',
            'district',
            'street',
            'address',
            'comment',
            'status',
            'inn',
            'contract_number',
            'email',
            "contact_full_name",
            "contact_phone_number"
        )
    