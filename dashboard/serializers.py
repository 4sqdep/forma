from rest_framework import serializers
from .models import (DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton,
                     ProjectDocumentation, NextStageDocuments, Files)


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


class FilesSerializer(serializers.ModelSerializer):
    """Fayllarni yuklash uchun serializer"""
    class Meta:
        model = Files
        fields = '__all__'


class MultipleFileUploadSerializer(serializers.Serializer):
    document_id = serializers.IntegerField()  # NextStageDocuments modelining IDsi
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False,
        write_only=True
    )

    def create(self, validated_data):
        document_id = validated_data.get('document_id')
        files = validated_data.get('files')

        # NextStageDocuments mavjudligini tekshirish
        try:
            document = NextStageDocuments.objects.get(id=document_id)
        except NextStageDocuments.DoesNotExist:
            raise serializers.ValidationError({"document_id": "NextStageDocuments not found."})

        # Fayllar ro'yxatini yaratish
        file_instances = [
            Files(
                document=document,
                user=self.context['request'].user,  # Foydalanuvchini olish
                files=file
            )
            for file in files
        ]

        # Fayllarni bir vaqtda bazaga qo'shish
        Files.objects.bulk_create(file_instances)

        return file_instances