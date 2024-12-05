from rest_framework import serializers
from .models import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton


class DashboardSubCategoryButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardSubCategoryButton
        fields = ['id', 'name', ]


class DashboardCategoryButtonSerializer(serializers.ModelSerializer):
    subcategories = DashboardSubCategoryButtonSerializer(many=True, source='dashboardsubcategorybutton_set')

    class Meta:
        model = DashboardCategoryButton
        fields = ['id', 'name', 'subcategories']


class DashboardButtonSerializer(serializers.ModelSerializer):
    categories = DashboardCategoryButtonSerializer(many=True, source='dashboardcategorybutton_set')

    class Meta:
        model = DashboardButton
        fields = ['id', 'name', 'categories']
