from decimal import Decimal
from rest_framework import serializers
from main.apps.dashboard.serializers.dashboard import ObjectSerializer
from main.apps.equipment.models.hydro_station import CalculationType, FinancialResource, FinancialResourceType, HydroStation
from django.db.models import Sum
from main.apps.equipment.models.industrial_equipment import IndustrialAsset






class HydroStationCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroStation 
        fields = (
            'id',
            'object',
            'supplier_name',
            'contract_number',
            'contract_amount',
            'file',
            'currency',
            'prepayment_from_own_fund',
            'prepayment_from_foreign_credit_account',
            'additional_prepayment',
            'payment_on_completion',
            'transit_equipment_amount',
            'delivery_date',
            'calculation_type',
            'financial_resource_data',
            'financial_reource_type'
        )

    
    def validate(self, attrs):
        financial_type = attrs.get('financial_resource_type')
        financial_data = attrs.get('financial_resource_data', [])

        required_titles = {"собственные средства", "кредитные средства"}
        if financial_type == FinancialResourceType.GES:
            if not isinstance(financial_data, list):
                raise serializers.ValidationError({
                    "financial_resource_data": "Must be a list of dictionaries."
                })

            existing_titles = {item.get("title") for item in financial_data}
            if existing_titles != required_titles:
                raise serializers.ValidationError({
                    "financial_resource_data": f"For 'funds', financial_resource_data must contain {required_titles}."
                })
        return attrs

    def calculate_financial_data(self, financial_data, contract_amount, calculation_type):
        own_funds = None
        credit_funds = None

        for item in financial_data:
            if item["title"] == "собственные средства":
                own_funds = item
            elif item["title"] == "кредитные средства":
                credit_funds = item

        if calculation_type == CalculationType.PERCENT:
            own_fund_percent = Decimal(own_funds.get("percent_or_amount", "0.00"))
            own_fund_amount = (contract_amount * own_fund_percent / Decimal(100)).quantize(Decimal("0.00"))

            remaining_percent = Decimal(100) - own_fund_percent
            credit_fund_amount = (contract_amount * remaining_percent / Decimal(100)).quantize(Decimal("0.00"))

            own_funds["amount"] = float(own_fund_amount)
            credit_funds["percent_or_amount"] = float(remaining_percent)
            credit_funds["amount"] = float(credit_fund_amount)

        elif calculation_type == CalculationType.AMOUNT:
            for item in financial_data:
                amount_value = Decimal(item.get("percent_or_amount", "0.00")).quantize(Decimal("0.00"))
                item["amount"] = float(amount_value)
        return financial_data
    

    def create(self, validated_data):
        financial_data = validated_data.get("financial_resource_data", [])
        contract_amount = Decimal(validated_data.get("contract_amount", "0.00"))
        calculation_type = validated_data.get("calculation_type")

        validated_data["financial_resource_data"] = self.calculate_financial_data(
            financial_data, contract_amount, calculation_type
        )
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        instance.object = validated_data.get("object", instance.object)
        instance.supplier_name = validated_data.get("supplier_name", instance.supplier_name)
        instance.contract_number = validated_data.get("contract_number", instance.contract_number)
        instance.contract_amount = validated_data.get("contract_amount", instance.contract_amount)
        instance.file = validated_data.get("file", instance.file)
        instance.currency = validated_data.get("currency", instance.currency)
        instance.prepayment_from_own_fund = validated_data.get("prepayment_from_own_fund", instance.prepayment_from_own_fund)
        instance.prepayment_from_foreign_credit_account = validated_data.get(
            "prepayment_from_foreign_credit_account", instance.prepayment_from_foreign_credit_account
        )
        instance.additional_prepayment = validated_data.get("additional_prepayment", instance.additional_prepayment)
        instance.payment_on_completion = validated_data.get("payment_on_completion", instance.payment_on_completion)
        instance.transit_equipment_amount = validated_data.get("transit_equipment_amount", instance.transit_equipment_amount)
        instance.delivery_date = validated_data.get("delivery_date", instance.delivery_date)
        instance.calculation_type = validated_data.get("calculation_type", instance.calculation_type)
        instance.financial_resource_type = validated_data.get("financial_resource_type", instance.financial_resource_type)

        financial_data = validated_data.get("financial_resource_data", instance.financial_resource_data)
        contract_amount = Decimal(instance.contract_amount)
        calculation_type = instance.calculation_type

        instance.financial_resource_data = self.calculate_financial_data(
            financial_data, contract_amount, calculation_type
        )
        instance.save()
        return instance
    


class HydroStationSerializer(serializers.ModelSerializer):
    object = ObjectSerializer()
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
            'prepayment_from_own_fund',
            'prepayment_from_foreign_credit_account',
            'additional_prepayment',
            'payment_on_completion',
            'transit_equipment_amount',
            'delivery_date',
            'calculation_type',
            'financial_resource_data',
            'total_delivered_amount',
            'delivered_amount_percent',
            'remained_delivered_amount',
            'remained_delivered_amount_percent',
            'latest_delivery_date'
        )

    def get_total_delivered_amount(self, obj):
        return (
            IndustrialAsset.objects.filter(equipment_category__hydro_station=obj, status='delivered')
            .aggregate(total=Sum('delivered_amount'))['total'] or 0.00
        )
    
    def get_transit_equipment_amount(self, obj):
        return (
            IndustrialAsset.objects.filter(equipment_category__hydro_station=obj, status='in_transit')
            .aggregate(total=Sum('expected_amount'))['total'] or 0.00
        )

    def get_delivered_amount_percent(self, obj):
        total_delivered_amount = Decimal(self.get_total_delivered_amount(obj))
        if obj.contract_amount:
            return round((total_delivered_amount * Decimal(100)) / obj.contract_amount, 2)
        return  Decimal("0.00")

    def get_remained_delivered_amount(self, obj):
        return obj.contract_amount - Decimal(self.get_total_delivered_amount(obj)) or Decimal("0.00")
    
    def get_remained_delivered_amount_percent(self, obj):
        return round(100 - self.get_delivered_amount_percent(obj), 2)

    def get_latest_delivery_date(self, obj):
        asset = IndustrialAsset.objects.filter(equipment_category__hydro_station=obj).order_by("-date").first()
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

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title name cannot be empty.")
        return value


