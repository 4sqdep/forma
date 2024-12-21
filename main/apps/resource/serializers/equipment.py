from main.apps.resource.serializers.measurement import MeasurementSerializer
from main.apps.resource.serializers.time_measurement import TimeMeasurementSerializer
from ...resource.models.equipment import Equipment, EquipmentCategory
from rest_framework import serializers 




class EquipmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory
        fields = (
            'id',
            'title',
        )


class EquipmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = (
            'equipment_category',
            'title',
            'measurement',
            'time_measurement'
        )


class EquipmentListSerializer(serializers.ModelSerializer):
    equipment_category = EquipmentCategorySerializer()
    measurement = MeasurementSerializer()
    time_measurement = TimeMeasurementSerializer()
    class Meta:
        model = Equipment
        fields = (
            'id',
            'equipment_category',
            'title',
            'measurement',
            'time_measurement'
        )
