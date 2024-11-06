from typing import Dict, Any

from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class Registerserializer(serializers.ModelSerializer):
    """Foydalanuvchi ro'yxatdan o'tish uchun"""
    class Meta:
        model = User
        fields = ('username', 'password')


class LoginSerializer(TokenObtainPairSerializer):
    """
    Ro'yxatdan o'tgan foydalanuvchilarni tizimga kirish uchun login serializer
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['id'] = self.user.id
        data['is_download'] = self.user.is_download
        return data