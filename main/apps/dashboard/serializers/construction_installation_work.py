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
    file_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ConstructionInstallationSection
        fields = (
            'id',
            'object',
            'title',
            'is_forma',
            'is_file',
            'file_name'
        )

    def get_file_name(self, obj):
        if obj.is_file:
            construction_installation_files = ConstructionInstallationFile.objects.filter(section=obj)[:4]
            file_name_list = [document_file.title for document_file in construction_installation_files]
            return file_name_list if file_name_list else []  
        if obj.is_forma:
            construction_installation_project = ConstructionInstallationProject.objects.filter(section=obj)[:4]
            project_name_list = [project_name.title for project_name in construction_installation_project]
            return project_name_list if project_name_list else [] 
        return [] 



class ConstructionInstallationStatisticsSerializer(serializers.ModelSerializer):
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