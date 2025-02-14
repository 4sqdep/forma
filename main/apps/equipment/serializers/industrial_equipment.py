from rest_framework import serializers
from main.apps.equipment.models.industrial_equipment import IndustrialAsset, IndustrialEquipment



class IndustrialEquipmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustrialEquipment 
        fields = (
            'id',
            'hydro_station',
            'title'
        )



class IndustrialEquipmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustrialEquipment 
        fields = (
            'id',
            'hydro_station',
            'title',
            'total_cost'
        )



class IndustrialAssetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustrialAsset
        fields = (
            'industrial_equipment',
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
            'industrial_equipment',
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

