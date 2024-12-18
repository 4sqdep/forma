from main.apps.resource.serializers.material import MaterialCategorySerializer, MaterialListSerializer
from main.apps.resource.serializers.measurement import MeasurementSerializer
from rest_framework import serializers 
from ...warehouse.models.material_warehouse import MaterialWarehouse



class MaterialWarehouseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialWarehouse
        fields = (
            'material_category',
            'material',
            'quantity',
            'measurement',
            'price_per_unit'
        )
    
    def create(self, validated_data):
        material_category = validated_data.get('material_category')
        material = validated_data.get('material')
        price_per_unit = validated_data.get('price_per_unit')

        existing_item = MaterialWarehouse.objects.filter(
            material_category=material_category,
            material=material,
            price_per_unit=price_per_unit
        ).first()

        if existing_item:
            existing_item.quantity += validated_data.get('quantity', 0)
            existing_item.total_price = existing_item.quantity * price_per_unit
            existing_item.save()
            return existing_item
        else:
            return super().create(validated_data)




class MaterialWarehouseListSerializer(serializers.ModelSerializer):
    material_category = MaterialCategorySerializer()
    material = MaterialListSerializer()
    measurement = MeasurementSerializer()
    class Meta:
        model = MaterialWarehouse
        fields = (
            'id',
            'material_category',
            'material',
            'quantity',
            'measurement',
            'price_per_unit',
            'total_price'
        )
    
    

class MaterialWarehouseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialWarehouse
        fields = (
            'material_category',
            'material',
            'quantity',
            'measurement',
            'price_per_unit'
        )