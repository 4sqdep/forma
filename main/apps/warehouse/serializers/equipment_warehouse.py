from main.apps.resource.serializers.equipment import EquipmentCategorySerializer, EquipmentListSerializer
from main.apps.resource.serializers.measurement import MeasurementSerializer
from main.apps.warehouse.models.equipment_warehouse import EquipmentWarehouse
from rest_framework import serializers 




class EquipmentWarehouseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentWarehouse
        fields = (
            'equipment_category',
            'equipment',
            'status',
            'quantity',
            'measurement',
            'time_measurement',
            'measurement_data'
        )



class EquipmentWarehouseListSerializer(serializers.ModelSerializer):
    equipment_category = EquipmentCategorySerializer()
    equipment = EquipmentListSerializer()
    measurement = MeasurementSerializer()
    class Meta:
        model = EquipmentWarehouse
        fields = (
            'id',
            'equipment_category',
            'equipment',
            'status',
            'quantity',
            'measurement',
            'time_measurement',
            'measurement_data'
        )
    

