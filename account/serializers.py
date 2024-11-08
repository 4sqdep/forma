from typing import Dict, Any

from rest_framework import serializers
from rest_framework.decorators import permission_classes

from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class Registerserializer(serializers.ModelSerializer):
    """Foydalanuvchi ro'yxatdan o'tish uchun"""
    class Meta:
        model = User
        fields = ('username', 'password')


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Department


class LoginSerializer(TokenObtainPairSerializer):
    """
    Ro'yxatdan o'tgan foydalanuvchilarni tizimga kirish uchun login serializer
    """

    department_name = serializers.SerializerMethodField()

    def get_department_name(self, obj):
        # Foydalanuvchiga tegishli bo'limni olish
        department = getattr(obj, 'department', None)
        if department:
            return department.name
        return None

    @classmethod
    def get_token(cls, user):
        # Token yaratish
        token = super().get_token(user)
        # Foydalanuvchiga tegishli ruxsatlarni olish
        permission = getattr(user, 'user_permission', None)

        # Token ichiga qo'shimcha ma'lumotlar qo'shish
        token['id'] = user.id
        token['is_download'] = user.is_download
        token['department_name'] = getattr(user.department, 'name', None)  # Foydalanuvchi bo'lim nomi
        token['role'] = user.department.name if user.department else None  # Foydalanuvchi lavozimi (rol)
        # Ruxsatlar mavjud bo'lsa, token ichiga qo'shish
        if permission:
            token['permissions'] = {
                'can_get': permission.can_get,
                'can_post': permission.can_post,
                'can_patch': permission.can_patch,
                'can_put': permission.can_put,
                'can_delete': permission.can_delete,
            }

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        # IP manzil va user-agentni olish
        ip_address = self.context['request'].META.get('REMOTE_ADDR')
        user_agent = self.context['request'].META.get('HTTP_USER_AGENT', 'unknown')

        # IP manzil va user-agentni token ichiga kiritish
        refresh['ip_address'] = ip_address
        refresh['user_agent'] = user_agent
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)  # access token
        return data
