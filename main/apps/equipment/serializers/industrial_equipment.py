from rest_framework import serializers
from main.apps.common.serializers import MeasurementSerializer
from main.apps.equipment.models.industrial_equipment import EquipmentSubCategory, IndustrialAsset, EquipmentCategory



class EquipmentCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory 
        fields = (
            'id',
            'hydro_station',
            'title',
            'has_subcategories'
        )
        read_only_fields = ('has_subcategories',)   
    


class EquipmentCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory 
        fields = (
            'id',
            'hydro_station',
            'title',
            'total_cost',
            'has_subcategories'
        )
    


class EquipmentSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentSubCategory 
        fields = (
            'id',
            'equipment_category',
            'title'
        )
    
    def create(self, validated_data):
        subcategory = EquipmentSubCategory.objects.create(**validated_data)

        if subcategory.equipment_category:
            subcategory.equipment_category.has_subcategories = True
            subcategory.equipment_category.save()
        return subcategory



class IndustrialAssetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustrialAsset
        fields = (
            'equipment_category',
            'equipment_subcategory',
            'object',
            'measurement',
            'text',
            'quantity',
            'country',
            'code',
            'price',
            'status',
            'delivered_amount',
            'date'
        )



class IndustrialAssetListSerializer(serializers.ModelSerializer):
    delivered_in_percent = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    remaining_in_percent = serializers.SerializerMethodField()
    measurement = MeasurementSerializer()
    currency_slug = serializers.CharField(source='equipment_category.hydro_station.currency.title')
    class Meta:
        model = IndustrialAsset
        fields = (
            'id',
            'equipment_category',
            'equipment_subcategory',
            'object',
            'measurement',
            'text',
            'quantity',
            'country',
            'code',
            'price',
            'status',
            'total_amount',
            'currency_slug',
            'delivered_amount',
            'delivered_in_percent',
            'remaining_amount',
            'remaining_in_percent',
            'date'
        )
    
    def get_delivered_in_percent(self, obj):
        if obj.total_amount == 0:
            return 0
        percent = (obj.delivered_amount / obj.total_amount) * 100
        return round(percent, 2)

    def get_remaining_amount(self, obj):
        return obj.total_amount - obj.delivered_amount
    
    def get_remaining_in_percent(self, obj):
        delivered_in_percent = self.get_delivered_in_percent(obj) or 0
        return max(0, 100 - delivered_in_percent)

         

