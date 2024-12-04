from rest_framework import serializers
from .models import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton


class DashboardButtonSerializer(serializers.ModelSerializer):
    """Assosiy button olish"""
    class Meta:
        model = DashboardButton
        fields = ['id', 'name']


class DashboardCategoryButtonSerializer(serializers.ModelSerializer):
    """Kategoriya buttonlar"""
    dashboard_button = DashboardButtonSerializer
    class Meta:
        model = DashboardCategoryButton
        fields = ['id', 'dashboard_button', 'name']


class DashboardSubCategoryButtonSerializer(serializers.ModelSerializer):
    """
    SubCategory button larni olish
    """
    dashboard_category_btn = DashboardCategoryButtonSerializer
    class Meta:
        model = DashboardSubCategoryButton
        fields = ['id', 'dashboard_category_btn', 'name']