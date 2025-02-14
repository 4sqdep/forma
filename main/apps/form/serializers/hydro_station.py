from rest_framework import serializers
from main.apps.equipment.models.hydro_station import FinancialResource, HydroStation
from django.db.models import Sum

from main.apps.equipment.models.industrial_equipment import IndustrialAsset


class HydroStationSerializer(serializers.ModelSerializer):
    total_delivered_amount = serializers.SerializerMethodField()
    delivered_amount_percent = serializers.SerializerMethodField()
    remained_delivered_amount = serializers.SerializerMethodField()
    remained_delivered_amount_percent = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    class Meta:
        model = HydroStation 
        fields = (
            'id',
            'dashboard_subbtn',
            'supplier_name',
            'contract_number',
            'contract_amount',
            'currency',
            'additional_amount',
            'delivery_date',
            'total_delivered_amount',
            'delivered_amount_percent',
            'remained_delivered_amount',
            'remained_delivered_amount_percent',
            'date'
        )

    def get_total_delivered_amount(self, obj):
        return (
            IndustrialAsset.objects.filter(industrial_equipment__hydro_station=obj)
            .aggregate(total=Sum('delivered_amount'))['total'] or 0.00
        )

    def get_delivered_amount_percent(self, obj):
        total_delivered_amount = self.get_total_delivered_amount(obj)
        contract_amount = obj.contract_amount
        return  (total_delivered_amount * 100) / contract_amount or 0.00

    def get_remained_delivered_amount(self, obj):
        contract_amount = obj.contract_amount
        total_delivered_amount = self.get_total_delivered_amount(obj)
        return contract_amount - total_delivered_amount or 0.00
    
    def get_remained_delivered_amount_percent(self, obj):
        delivered_amount_percent = self.get_delivered_amount_percent(obj)
        return (100 - delivered_amount_percent) or 0.00

    def get_date(self, obj):
        asset = IndustrialAsset.objects.filter(industrial_equipment__hydro_station=obj).first()
        return asset.date if asset else None  




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

