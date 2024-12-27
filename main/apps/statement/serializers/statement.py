from main.apps.account.serializer import UserDetailSerializer
from main.apps.location.serializer import CountrySerializer, DistrictSerializer, RegionSerializer
from main.apps.statement.models.statement import Statement
from rest_framework import serializers 



class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = (
            'id',
            'employee',
            "client_type",
            'full_name',
            'phone_number',
            'country',
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
    employee = UserDetailSerializer()
    country = CountrySerializer()
    region = RegionSerializer()
    district = DistrictSerializer()
    class Meta:
        model = Statement
        fields = (
            'id',
            'employee',
            "client_type",
            'full_name',
            'phone_number',
            'country',
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
            'id',
            'employee',
            'client_type',
            'full_name',
            'phone_number',
            'country',
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
    