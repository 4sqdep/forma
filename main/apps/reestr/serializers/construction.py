from rest_framework import serializers
from main.apps.reestr.models.construction import ConstructionTask, MonthlyExpense



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

