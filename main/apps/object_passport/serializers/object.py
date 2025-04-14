from rest_framework import serializers
from main.apps.object_passport.models.object import Object




class ObjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = (
            'object_category',
            'object_subcategory',
            'currency',
            'title',
            'community_fund',
            'foreign_loan',
            'construction_work_amount',
            'equipment_amount',
            'other_expense',
            'total_price',
            'object_power',
            'annual_electricity_production',
            'pressure',
            'water_consumption',
            'object_file',
            'useful_work_coefficient',
            'latitude',
            'longitude',
            'start_date',
            'end_date',
        )


class ObjectSerializer(serializers.ModelSerializer):
    currency_slug = serializers.CharField(source='currency.slug_title', read_only=True)
    class Meta:
        model = Object
        fields = (
            'id',
            'object_category',
            'object_subcategory',
            'currency',
            'currency_slug',
            'title',
            'community_fund',
            'foreign_loan',
            'construction_work_amount',
            'equipment_amount',
            'other_expense',
            'total_price',
            'object_power',
            'annual_electricity_production',
            'pressure',
            'water_consumption',
            'object_file',
            'useful_work_coefficient',
            'latitude',
            'longitude',
            'start_date',
            'end_date',
        )

