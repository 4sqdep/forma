from rest_framework import serializers
from main.apps.reestr.models.construction import ConstructionTask, MonthlyExpense
from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce
from decimal import Decimal


class ConstructionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionTask 
        fields = (
            'id',
            'next_stage_document',
            'employee',
            'currency',
            'title',
            'total_cost'
        )


class MonthlyExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyExpense
        fields = (
            'construction_task',
            'spent_amount',
            'date'
        )
    
    def validate(self, data):
        construction_task = data.get('construction_task')
        spent_amount = data.get('spent_amount')

        if construction_task and spent_amount:
            total_cost = construction_task.total_cost or Decimal(0)

            fact_sum = MonthlyExpense.objects.filter(construction_task=construction_task).aggregate(
                        total_spent=Coalesce(Sum("spent_amount"), Decimal(0))
                    )["total_spent"]
            
            remaining_budget = total_cost - fact_sum

            if spent_amount > remaining_budget:
                raise serializers.ValidationError(
                    {"spent_amount": "You cannot add more than the remaining budget."}
                    )
        return data
        


class MonthlyExpenseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyExpense
        fields = (
            'id',
            'construction_task',
            'spent_amount',
            'date'
        )
    
    def update(self, instance, validated_data):
        instance.construction_task = validated_data.get('construction_task', instance.construction_task)
        instance.spent_amount = validated_data.get('spent_amount', instance.spent_amount)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance

