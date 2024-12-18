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
            'payment_for_employment',
            'payment_from_client',
            'discount_percent',
            'discount_sum'
        )
        


class CheckListSerializer(serializers.ModelSerializer):
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
            'equipment',
            'equipment_total_price',
            'payment_for_employment',
            'payment_from_client',
            'discount_percent',
            'discount_sum'
        )

