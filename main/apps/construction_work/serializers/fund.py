from rest_framework import serializers
from main.apps.construction_work.models.fund import ConstructionInstallationProject, MonthlyCompletedTask
from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce
from decimal import Decimal





class ConstructionInstallationProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionInstallationProject
        fields = (
            "id", 
            "section", 
            "title", 
            "currency", 
            "allocated_amount", 
        )



class MonthlyCompletedTaskSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y", input_formats=["%Y-%m-%d"], required=False)
    class Meta:
        model = MonthlyCompletedTask
        fields = (
            "id", 
            "construction_installation_project", 
            "date", 
            "monthly_amount", 
        )

    def validate(self, data):
        construction_installation_project = data.get('construction_installation_project')
        monthly_amount = data.get('monthly_amount')
        date = data.get('date')

        if construction_installation_project and monthly_amount and date:
            existing_completed_task = MonthlyCompletedTask.objects.filter(
                construction_installation_project=construction_installation_project,
                date__year=date.year,
                date__month=date.month
            ).exists()

            if existing_completed_task:
                raise serializers.ValidationError(
                    {"date": "Bu oyning bajarilgan ishlar xarajati allaqachon qo'shilgan"}
                )
            
            allocated_amount = construction_installation_project.allocated_amount or Decimal(0)
            fact_sum = MonthlyCompletedTask.objects.filter(
                construction_installation_project=construction_installation_project
            ).aggregate(total_spent=Coalesce(Sum('monthly_amount'), Decimal(0)))['total_spent']

            remaining_budget = allocated_amount - fact_sum

            if monthly_amount > remaining_budget:
                raise serializers.ValidationError(
                    {'allocated_amount': "Siz qolgan byudjetdan ko‘proq qo‘sha olmaysiz."}
                )
        return data