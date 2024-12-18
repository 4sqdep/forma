from rest_framework import serializers 
from .models import ServiceCategory, Service
from django.utils.translation import gettext_lazy as _



class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = (
            'id',
            'title'
        )


class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'service_category',
            'title',
            'equipment_category',
            'material_category',
            'equipment',
            'material',
            'service_price',
            'lead_time'
        )

    def validate(self, attrs):
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



class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'id',
            'service_category',
            'title',
            'equipment_category',
            'material_category',
            'equipment',
            'material',
            'service_price',
            'lead_time'
        )

