from rest_framework import serializers
from main.apps.construction_work.models.statistics import ConstructionInstallationStatistics




class ConstructionInstallationStatisticsSerializer(serializers.ModelSerializer):
    currency_slug = serializers.CharField(source='object.currency.slug_title', read_only=True)
    date = serializers.DateField(format="%d-%m-%Y", input_formats=["%Y-%m-%d"], required=False)
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