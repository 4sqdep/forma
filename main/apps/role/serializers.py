from rest_framework import serializers
from main.apps.object_passport.serializers.object import ObjectSerializer
from main.apps.role.models import Role






class RoleListSerializer(serializers.ModelSerializer):
    # employee = serializers.CharField(source='employee.full_name')
    employee = serializers.SerializerMethodField()
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
    
    def get_employee_full_name(self, obj):
        if obj.employee:
            return obj.employee.full_name
        return None



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