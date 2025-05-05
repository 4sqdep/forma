from rest_framework import serializers
from main.apps.object_passport.serializers.object import ObjectSerializer
from main.apps.role.models import Role






class RoleListSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee.full_name')
    object = ObjectSerializer(many=True)
    
    class Meta:
        model = Role 
        fields = (
            'id',
            'employee',
            'object',
            'has_construction_work',
            'has_project_document',
            'has_equipment',
            'has_contract',
            'can_create',
            'can_update',
            'can_delete'
        )



class RoleUpdateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Role 
        fields = (
            'id',
            'employee',
            'object',
            'has_construction_work',
            'has_project_document',
            'has_equipment',
            'has_contract',
            'can_create',
            'can_update',
            'can_delete'
        )