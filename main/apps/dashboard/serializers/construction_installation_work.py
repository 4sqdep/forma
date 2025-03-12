from rest_framework import serializers
from main.apps.dashboard.models.construction_installation_work import (
    ConstructionInstallationFile,
    ConstructionInstallationProject,  
    ConstructionInstallationSection,
    ConstructionInstallationStatistics,
    MonthlyCompletedTask
)
from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce
from decimal import Decimal




class ConstructionInstallationSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionInstallationSection
        fields = (
            'id',
            'object',
            'title',
            'is_forma',
            'is_file'
        )



class ConstructionInstallationStatisticsSerializer(serializers.ModelSerializer):
    # contract_file = serializers.SerializerMethodField()
    currency_slug = serializers.CharField(source='object.currency.slug_title', read_only=True)
    class Meta:
        model = ConstructionInstallationStatistics
        fields = (
            'id',
            'object',
            'installation_work_amount',
            'date',
            'remanied_work_amount',
            'cost_of_performed_work',
            'currency_slug',
            'contract_file',
            'contractor'
        )
    
    # def get_contract_file(self, obj):
    #     if obj.contract_file:
    #         request = self.context.get('request')
    #         return request.build_absolute_uri(obj.contract_file.url) if request else obj.contract_file.url
    #     return None


class ConstructionInstallationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionInstallationFile
        fields = (
            "id", 
            "section", 
            "title", 
            "date", 
            "file_code", 
            "file", 
        )


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

        if construction_installation_project and monthly_amount:
            allocated_amount = construction_installation_project.allocated_amount or Decimal(0)

            fact_sum = MonthlyCompletedTask.objects.filter(construction_installation_project=construction_installation_project).aggregate(
                total_spent=Coalesce(Sum('monthly_amount'), Decimal(0))
            )

            remaining_budget = allocated_amount - fact_sum

            if monthly_amount > remaining_budget:
                raise serializers.ValidationError(
                    {'allocated_amount': "You cannot add more than the remaining budget."}
                )
        return data