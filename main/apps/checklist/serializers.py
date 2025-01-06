from main.apps.resource.serializers.equipment import EquipmentCategorySerializer, EquipmentListSerializer
from main.apps.resource.serializers.time_measurement import TimeMeasurementSerializer
from main.apps.service.serializers import ServiceCategorySerializer, ServiceListSerializer
from main.apps.statement.serializers.statement import StatementListSerializer
from main.apps.warehouse.models.equipment_warehouse import EquipmentWarehouse
from rest_framework import serializers 
from django.utils.translation import gettext_lazy as _
from .models import CheckList
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta


class CheckListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = (
            'statement',
            'building_type',
            'building_area',
            'service_category',
            'service',
            'equipment',
            'measurement',
            'payment_for_employment',
            'payment_from_client',
            'discount_percent',
            'discount_sum',
            'service_data'
        )
        


class CheckListSerializer(serializers.ModelSerializer):
    statement = StatementListSerializer()
    service = ServiceListSerializer(many=True)
    service_category = ServiceCategorySerializer(many=True)
    equipment = EquipmentListSerializer(many=True)
    equipment_category = EquipmentCategorySerializer(many=True)
    measurement = TimeMeasurementSerializer()
    created_by = serializers.CharField(source='created_by.get_full_name', read_only=True)
    service_total_price = serializers.SerializerMethodField()
    equipment_price = serializers.SerializerMethodField()
    equipment_count = serializers.SerializerMethodField()
    service_count = serializers.SerializerMethodField()
    class Meta:
        model = CheckList
        fields = (
            'id',
            'statement',
            'building_type',
            'building_area',
            'service_category',
            'service',
            'service_count',
            'service_total_price',
            'equipment_category',
            'equipment',
            'measurement',
            'equipment_total_price',
            'payment_for_employment',
            'payment_from_client',
            'discount_percent',
            'discount_sum',
            'created_by',
            'equipment_price',
            'equipment_count',
            'service_data'
        )
    
    def get_equipment_price(self, obj):
        price = 0
        if not obj.measurement:
            return None 
        for equipment in obj.equipment.all():
            equipment_warehouse = EquipmentWarehouse.objects.filter(equipment=equipment).first()
            if equipment_warehouse and equipment_warehouse.measurement_data:
                price = equipment_warehouse.measurement_data.get(obj.measurement.title)
        return price
    

    def get_equipment_count(self, obj):
        quantity = 0
        for equipment in obj.equipment.all():
            equipment_warehouse = EquipmentWarehouse.objects.filter(equipment=equipment).first()
            if equipment_warehouse:
                quantity = equipment_warehouse.quantity
        return quantity


    def get_service_count(self, obj):
        service_count = obj.service.all().count()
        return service_count
    

    def get_service_total_price(self, obj):
        total_price = 0
        service_data = obj.service_data
        for service_id, quantity in service_data.items():
            service = obj.service.filter(id=service_id).first()
            if service:
                total_price += service.service_price * quantity
        return total_price

