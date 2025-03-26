from main.apps.dashboard.models.dashboard import ObjectCategory, ObjectSubCategory, Object
from main.apps.dashboard.models.document import NextStageDocuments
from main.apps.account.models.user import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Foydalanuvchi malumotlarini olish uchun serializers"""
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class ObjectCategoryNameSerializer(serializers.ModelSerializer):
    """"Asosiy button name olish uchun serializer"""
    class Meta:
        model = ObjectCategory
        fields = ['id', 'name']


class ObjectSubCategoryNameSerializer(serializers.ModelSerializer):
    """"Kategoriya button name olish uchun serializer"""
    class Meta:
        model = ObjectSubCategory
        fields = ['id', 'name']


class ObjectNameSerializer(serializers.ModelSerializer):
    """"Sub - Kategoriya button name olish uchun serializer"""
    class Meta:
        model = Object
        fields = ['id', 'name']



class NextStageDocumentsSerializer(serializers.ModelSerializer):
    """Keyingi hujjatlar uchun serializer"""
    # object_name = ObjectNameSerializer(source='subcategories_btn', read_only=True)
    class Meta:
        model = NextStageDocuments
        fields = ['id',  'name', 'is_forma', 'is_section', 'is_file']


class SearchObjectsNameSerializer(serializers.ModelSerializer):
    """Obyekt nomlarini izlash uchun serializer"""
    class Meta:
        model = Object
        fields = ['id', 'name']

