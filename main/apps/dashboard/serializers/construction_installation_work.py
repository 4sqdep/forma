from rest_framework import serializers
from main.apps.dashboard.models.construction_installation_work import (
    ConstructionInstallationFile,
    ConstructionInstallationProject,  
    ConstructionInstallationSection,
    ConstructionInstallationStatistics,
    ConstructionInstallationSubSection,
    MonthlyCompletedTask
)



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
    class Meta:
        model = ConstructionInstallationStatistics
        fields = (
            'id',
            'object',
            'installation_work_amount',
            'date',
            'remanied_work_amount',
            'cost_of_performed_work',
            'contract_file',
            'contractor'
        )


class ConstructionInstallationSubSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionInstallationSubSection
        fields = (
            "id", 
            "construction_installation_section", 
            "title", 
        )


class ConstructionInstallationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionInstallationFile
        fields = (
            "id", 
            "sub_section", 
            "title", 
            "full_name", 
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