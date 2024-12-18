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
    class Meta:
        model = Equipment
        fields = (
            'id',
            'equipment_category',
            'title',
            'measurement',
            'time_measurement'
        )
