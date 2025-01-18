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
            'spen_amount'
        )


class MonthlyExpenseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyExpense
        fields = (
            'id',
            'year',
            'month',
            'construction_task',
            'spen_amount',
            'amount',
            'total_year_amount',
            'total_fact',
            'total_fact_amount',
            'amount_differece',
            'total_amount_difference'
        )

