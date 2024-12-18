from main.apps.checklist.serializers import CheckListSerializer
from rest_framework import serializers 
from .models import Order




class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'checklist',
            'profitability_of_order',
            'total_lead_time',
            'order_comment',
            'employee_note'
        )



class OrderListSerializer(serializers.ModelSerializer):
    checklist = CheckListSerializer()
    class Meta:
        model = Order
        fields = (
            'id',
            'checklist',
            'profitability_of_order',
            'total_lead_time',
            'order_comment',
            'employee_note'
        )

