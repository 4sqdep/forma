from rest_framework import serializers
from main.apps.equipment.models.industrial_equipment import EquipmentSubCategory, IndustrialAsset, EquipmentCategory



class EquipmentCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory 
        fields = (
            'id',
            'hydro_station',
            'title'
        )



class EquipmentCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory 
        fields = (
            'id',
            'hydro_station',
            'title',
            'total_cost'
        )


class EquipmentSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentSubCategory 
        fields = (
            'id',
            'equipment_category',
            'title'
        )



class IndustrialAssetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustrialAsset
        fields = (
            'equipment_category',
            'equipment_subcategory',
            'measurement',
            'text',
            'quantity',
            'country',
            'code',
            'price',
            'delivered_amount',
            'delivered_in_percent',
            'remaining_amount',
            'remaining_in_percent',
            'expected_amount',
            'date'
        )



class IndustrialAssetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustrialAsset
        fields = (
            'id',
            'equipment_category',
            'equipment_subcategory',
            'measurement',
            'text',
            'quantity',
            'country',
            'code',
            'price',
            'total_amount',
            'delivered_amount',
            'delivered_in_percent',
            'remaining_amount',
            'remaining_in_percent',
            'expected_amount',
            'date'
        )

