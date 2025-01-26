from main.apps.dashboard.models.dashboard import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton
from main.apps.dashboard.models.document import ProjectDocumentation, NextStageDocuments
from main.apps.main.models import Files
from main.apps.main.models import ObjectsPassword
from main.apps.account.models.user import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Foydalanuvchi malumotlarini olish uchun serializers"""
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class DashboardButtonNameSerializer(serializers.ModelSerializer):
    """"Asosiy button name olish uchun serializer"""
    class Meta:
        model = DashboardButton
        fields = ['id', 'name']


class DashboardCategoryButtonNameSerializer(serializers.ModelSerializer):
    """"Kategoriya button name olish uchun serializer"""
    class Meta:
        model = DashboardCategoryButton
        fields = ['id', 'name']


class DashboardSubCategoryButtonNameSerializer(serializers.ModelSerializer):
    """"Sub - Kategoriya button name olish uchun serializer"""
    class Meta:
        model = DashboardSubCategoryButton
        fields = ['id', 'name']


class ProjectDocumentationNameSerializer(serializers.ModelSerializer):
    """Bo'lim nomini olish uchun serializer"""
    class Meta:
        model = ProjectDocumentation
        fields = ['id', 'name']


class GetObjectsPasswordSerializer(serializers.ModelSerializer):
    """Obyekt pasportiga tegishlim malumotlarni olish uchun serializer"""
    user = UserSerializer(read_only=True)
    object_name = DashboardSubCategoryButtonNameSerializer(source='subcategory_btn', read_only=True)
    class Meta:
        model = ObjectsPassword
        fields = ['id', 'user', 'object_name', 'smr_price', 'equipment_price', 'investment_price', 'uge_price',
                  'total_price', 'total_power', 'start_date', 'end_date', 'created_at']


class CreateObjectsPasswordSerializer(serializers.ModelSerializer):
    """Obyekt pasportini kiritish uchun serializer"""
    class Meta:
        model = ObjectsPassword
        fields = ['id', 'main_btn', 'category_btn', 'subcategory_btn', 'project_documentation',
                  'smr_price', 'equipment_price', 'investment_price',
                  'uge_price', 'total_price', 'total_power', 'start_date', 'end_date',]


class FilesCreateSerializer(serializers.ModelSerializer):
    """Fayl yuklash uchun serializer"""
    class Meta:
        model = Files
        fields = ['obj_password', 'file']


class GetFilesSerializer(serializers.ModelSerializer):
    """Faylni olish uchun serializer"""
    class Meta:
        model = Files
        fields = ['id', 'obj_password', 'file']


class NextStageDocumentsSerializer(serializers.ModelSerializer):
    """Keyingi hujjatlar uchun serializer"""
    object_name = DashboardSubCategoryButtonNameSerializer(source='subcategories_btn', read_only=True)
    class Meta:
        model = NextStageDocuments
        fields = ['id', 'object_name', 'name']