from decimal import Decimal
from rest_framework import serializers
from main.apps.equipment.models.hydro_station import FinancialResource, HydroStation
from django.db.models import Sum
from main.apps.equipment.models.industrial_equipment import IndustrialAsset




class HydroStationSerializer(serializers.ModelSerializer):
    total_delivered_amount = serializers.SerializerMethodField()
    transit_equipment_amount = serializers.SerializerMethodField()
    delivered_amount_percent = serializers.SerializerMethodField()
    remained_delivered_amount = serializers.SerializerMethodField()
    remained_delivered_amount_percent = serializers.SerializerMethodField()
    latest_delivery_date = serializers.SerializerMethodField()
    class Meta:
        model = HydroStation 
        fields = (
            'id',
            'object',
            'supplier_name',
            'contract_number',
            'contract_amount',
            'currency',
            'transit_equipment_amount',
            'delivery_date',
            'total_delivered_amount',
            'delivered_amount_percent',
            'remained_delivered_amount',
            'remained_delivered_amount_percent',
            'latest_delivery_date'
        )

    def get_total_delivered_amount(self, obj):
        return (
            IndustrialAsset.objects.filter(industrial_equipment__hydro_station=obj, status='delivered')
            .aggregate(total=Sum('delivered_amount'))['total'] or 0.00
        )
    
    def get_transit_equipment_amount(self, obj):
        return (
            IndustrialAsset.objects.filter(industrial_equipment__hydro_station=obj, status='in_transit')
            .aggregate(total=Sum('transit_equipment_amount'))['total'] or 0.00
        )

    def get_delivered_amount_percent(self, obj):
        total_delivered_amount = self.get_total_delivered_amount(obj)
        if obj.contract_amount:
            return round((total_delivered_amount * 100) / obj.contract_amount, 2)
        return  Decimal("0.00")

    def get_remained_delivered_amount(self, obj):
        return obj.contract_amount - self.get_total_delivered_amount(obj) or Decimal("0.00")
    
    def get_remained_delivered_amount_percent(self, obj):
        return round(100 - self.get_delivered_amount_percent(obj), 2)

    def get_latest_delivery_date(self, obj):
        asset = IndustrialAsset.objects.filter(industrial_equipment__hydro_station=obj).order_by("-date").first()
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

