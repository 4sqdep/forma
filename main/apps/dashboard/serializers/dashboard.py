from rest_framework import serializers
from main.apps.dashboard.models.dashboard import (
    DashboardButton, 
    DashboardCategoryButton, 
    DashboardSubCategoryButton
)



class DashboardButtonSerializer(serializers.ModelSerializer):
    """Assosiy button olish"""
    category_count = serializers.IntegerField(read_only=True)
    has_data = serializers.BooleanField(read_only=True)
    class Meta:
        model = DashboardButton
        fields = (
            'id', 
            'name', 
            'category_count', 
            'has_data'
        )


class DashboardCategoryButtonSerializer(serializers.ModelSerializer):
    """Kategoriya buttonlar"""
    dashboard_button = DashboardButtonSerializer
    subcategory_count = serializers.IntegerField(read_only=True)
    has_data = serializers.BooleanField(read_only=True)
    class Meta:
        model = DashboardCategoryButton
        fields = (
            'id', 
            'dashboard_button', 
            'name', 
            'subcategory_count', 
            'has_data'
        )


class DashboardSubCategoryButtonSerializer(serializers.ModelSerializer):
    """
    SubCategory button larni olish
    """
    dashboard_category_btn = DashboardCategoryButtonSerializer
    class Meta:
        model = DashboardSubCategoryButton
        fields = (
            'id', 
            'dashboard_category_btn', 
            'name'
        )


class DashboardSubCategoryButtonSerializerName(serializers.ModelSerializer):
    """Faqan name fildni olish"""
    class Meta:
        model = DashboardSubCategoryButton
        fields = (
            'id', 
            'name'
        )
