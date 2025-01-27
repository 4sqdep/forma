from rest_framework import serializers
from main.apps.reestr.models.construction import ConstructionTask, MonthlyExpense



class ConstructionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionTask 
        fields = (
            'id',
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

