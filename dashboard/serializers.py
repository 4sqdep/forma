from rest_framework import serializers
from .models import (DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton,
                     ProjectDocumentation, NextStageDocuments)


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


class DashboardSubCategoryButtonSerializerName(serializers.ModelSerializer):
    """Faqan name fildni olish"""
    class Meta:
        model = DashboardSubCategoryButton
        fields = ['id', 'name']


class ProjectDocumentationSerializer(serializers.ModelSerializer):
    subcategories_btn = DashboardSubCategoryButtonSerializerName()
    class Meta:
        model = ProjectDocumentation

        fields = ['id', 'user', 'subcategories_btn', 'name', 'created_at']


class NextStageDocumentsSerializer(serializers.ModelSerializer):
    """Keyingi hujjatlar uchun serializer"""
    class Meta:
        model = NextStageDocuments
        fields = ['id', 'name']

class NextStageDocumentsCreateSerializer(serializers.ModelSerializer):
    """Keyingi hujjatlar uchun papakalar yaratish uchun serializer"""
    class Meta:
        model = NextStageDocuments
        fields = ['id', 'project_document', 'subcategories_btn', 'name']