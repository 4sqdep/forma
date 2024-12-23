from main.apps.resource.serializers.equipment import EquipmentCategorySerializer, EquipmentListSerializer
from main.apps.resource.serializers.time_measurement import TimeMeasurementSerializer
from main.apps.service.serializers import ServiceCategorySerializer, ServiceListSerializer
from main.apps.statement.serializers.statement import StatementListSerializer
from rest_framework import serializers 
from django.utils.translation import gettext_lazy as _
from .models import CheckList



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
            'discount_sum'
        )
        


class CheckListSerializer(serializers.ModelSerializer):
    statement = StatementListSerializer()
    service = ServiceListSerializer()
    service_category = ServiceCategorySerializer()
    equipment = EquipmentListSerializer()
    equipment_category = EquipmentCategorySerializer()
    measurement = TimeMeasurementSerializer()
    class Meta:
        model = CheckList
        fields = (
            'id',
            'statement',
            'building_type',
            'building_area',
            'service_category',
            'service',
            'service_total_price',
            'equipment_category',
            'equipment',
            'measurement',
            'equipment_total_price',
            'payment_for_employment',
            'payment_from_client',
            'discount_percent',
            'discount_sum'
        )

