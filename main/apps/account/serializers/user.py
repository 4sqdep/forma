from typing import Dict, Any
from main.apps.account.models.user import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class Registerserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 
            'password'
        )



class LoginSerializer(TokenObtainPairSerializer):
    department_name = serializers.SerializerMethodField()

    def get_department_name(self, obj):
        department = getattr(obj, 'department', None)
        if department:
            return department.name
        return None

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        permission = getattr(user, 'user_permission', None)

        token['id'] = user.id
        token['is_download'] = user.is_download
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
        ip_address = self.context['request'].META.get('REMOTE_ADDR')
        user_agent = self.context['request'].META.get('HTTP_USER_AGENT', 'unknown')

        refresh['ip_address'] = ip_address
        refresh['user_agent'] = user_agent
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 
            'first_name', 
            'last_name', 
            'username',
            'email', 
            'phone', 
            'image'
        )



class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'