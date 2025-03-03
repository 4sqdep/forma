from rest_framework import serializers
from main.apps.common.serializers import CurrencySerializer
from main.apps.dashboard.serializers.dashboard import ObjectSerializer
from main.apps.form.models.form3 import Form3




class Form3CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form3 
        fields = (
            'object',
            'currency',
            'total_amount',
            'total_amount_year',
            'vat',
            'work_volume_from_construction_beginning',
            'current_contract_amount_from_construction_beginning',
            'work_volume_from_year_beginnging',
            'current_contract_amount_from_year_beginnging',
            'work_volume_for_month',
            'current_contract_amount_for_month'
        )



class Form3ListSerializer(serializers.ModelSerializer):
    object = ObjectSerializer()
    currency = CurrencySerializer()
    work_volume_from_construction_beginning = serializers.SerializerMethodField()
    work_volume_from_year_beginnging = serializers.SerializerMethodField()
    work_volume_for_month = serializers.SerializerMethodField()

    class Meta:
        model = Form3 
        fields = (
            'id',
            'object',
            'currency',
            'total_amount',
            'total_amount_year',
            'vat',
            'work_volume_from_construction_beginning',
            'current_contract_amount_from_construction_beginning',
            'work_volume_from_year_beginnging',
            'current_contract_amount_from_year_beginnging',
            'work_volume_for_month',
            'current_contract_amount_for_month'
        )
    
    def get_work_volume_from_construction_beginning(self, obj):
        return round((obj.current_contract_amount_from_construction_beginning / obj.total_amount) * 100)
    

    def get_work_volume_from_year_beginnging(self, obj):
        return round((obj.current_contract_amount_from_year_beginnging / obj.current_contract_amount_from_construction_beginning) * 100)
    

    def get_work_volume_for_month(self, obj):
        return round((obj.current_contract_amount_for_month / obj.total_amount_year) * 100)
    

    







