from main.apps.account.serializer import UserDetailSerializer
from main.apps.resource.serializers.equipment import EquipmentCategorySerializer, EquipmentListSerializer
from main.apps.resource.serializers.material import MaterialCategorySerializer, MaterialListSerializer
from main.apps.resource.serializers.measurement import MeasurementSerializer
from rest_framework import serializers 
from django.utils.translation import gettext_lazy as _
from .models import ResourceRequest, ResourceReturn



def validate_resource(attrs):
    equipment_category = attrs.get('equipment_category')
    material_category = attrs.get('material_category')
    equipment = attrs.get('equipment')
    material = attrs.get('material')

    if equipment_category and material_category:
        raise serializers.ValidationError(
            _('You cannot select both Equipment Category and Material Category.')
        )

    if equipment_category and not equipment:
        raise serializers.ValidationError(
            _('If Equipment Category is selected, Equipment is required.')
        )

    if material_category and not material:
        raise serializers.ValidationError(
            _('If Material Category is selected, Material is required.')
        )

    if not equipment_category and not material_category:
        raise serializers.ValidationError(
            _('You must select either Equipment Category or Material Category.')
        )
    return attrs



class ResourceRequestListSerializer(serializers.ModelSerializer):
    sender = UserDetailSerializer()
    receiver = UserDetailSerializer()
    equipment_category = EquipmentCategorySerializer()
    equipment = EquipmentListSerializer()
    material_category = MaterialCategorySerializer()
    material = MaterialListSerializer()
    measurement = MeasurementSerializer()
    class Meta:
        model = ResourceRequest
        fields = (
            'id',
            'sender',
            'receiver',
            'request_for',
            'text',
            'equipment_category',
            'equipment',
            'material_category',
            'material',
            'quantity',
            'pickup_time',
            'return_time',
            'status',
            'measurement'
        )



class ResourceRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceRequest
        fields = (
            'sender',
            'receiver',
            'request_for',
            'text',
            'equipment_category',
            'equipment',
            'material_category',
            'material',
            'quantity',
            'pickup_time',
            'return_time',
            'status',
            'measurement'
        )

    def validate(self, attrs):
        return validate_resource(attrs)



class ResourceReturnListSerializer(serializers.ModelSerializer):
    sender = UserDetailSerializer()
    receiver = UserDetailSerializer()
    equipment_category = EquipmentCategorySerializer()
    equipment = EquipmentListSerializer()
    material_category = MaterialCategorySerializer()
    material = MaterialListSerializer()
    measurement = MeasurementSerializer()
    class Meta:
        model = ResourceReturn
        fields = (
            'id',
            'sender',
            'receiver',
            'request_for',
            'text',
            'equipment_category',
            'equipment',
            'material_category',
            'material',
            'quantity',
            'pickup_time',
            'return_time',
            'status',
            'measurement'
        )



class ResourceReturnCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceReturn
        fields = (
            'sender',
            'receiver',
            'request_for',
            'text',
            'equipment_category',
            'equipment',
            'material_category',
            'material',
            'quantity',
            'pickup_time',
            'return_time',
            'status',
            'measurement'
        )

    def validate(self, attrs):
        return validate_resource(attrs)



