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
            'year',
            'month',
            'construction_task',
            'spent_amount'
        )


class MonthlyExpenseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyExpense
        fields = (
            'id',
            'year',
            'month',
            'construction_task',
            'spent_amount',
            'amount',
            # 'total_year',
            # 'total_fact',
            # 'total_fact_amount',
            # 'difference_amount',
            # 'total_difference_amount'
        )

