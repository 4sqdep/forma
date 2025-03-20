from rest_framework import serializers
from main.apps.dashboard.models.dashboard import (
    ObjectCategory, 
    ObjectSubCategory, 
    Object
)



class ObjectCategorySerializer(serializers.ModelSerializer):
    category_count = serializers.IntegerField(read_only=True)
    has_data = serializers.BooleanField(read_only=True)
    class Meta:
        model = ObjectCategory
        fields = (
            'id', 
            'name', 
            'slug_name',
            'category_count', 
            'has_data'
        )



class ObjectSubCategorySerializer(serializers.ModelSerializer):
    object_category = ObjectCategorySerializer
    subcategory_count = serializers.IntegerField(read_only=True)
    has_data = serializers.BooleanField(read_only=True)
    class Meta:
        model = ObjectSubCategory
        fields = (
            'id', 
            'object_category', 
            'name', 
            'subcategory_count', 
            'has_data'
        )



class ObjectSerializer(serializers.ModelSerializer):
    currency_slug = serializers.CharField(source='currency.slug_title', read_only=True)
    class Meta:
        model = Object
        fields = (
            'id',
            'object_category',
            'object_subcategory',
            'project_documentation',
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
            'start_date',
            'end_date',
        )

