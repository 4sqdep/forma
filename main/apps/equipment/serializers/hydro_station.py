from rest_framework import serializers
from main.apps.equipment.models.hydro_station import FinancialResource, HydroStation



class HydroStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroStation 
        fields = (
            'id',
            'title',
            'supplier_name',
            'contract_number',
            'contract_amount',
            'currency',
            'additional_amount',
            'delivery_date'
        )


class FinancialResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialResource
        fields = (
            'id',
            'hydro_station',
            'title',
            'amount',
            'prepayment_from_own_fund',
            'prepayment_from_foreign_credit_account',
            'additional_prepayment',
            'payment_on_completion'
        )

