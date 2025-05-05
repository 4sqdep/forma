from rest_framework import serializers
from main.apps.object_passport.models.object import Object
from main.apps.object_passport.serializers.object import ObjectSerializer
from main.apps.role.models import Role






class RoleSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee.full_name', read_only=True)
    object = serializers.PrimaryKeyRelatedField(queryset=Object.objects.all(), many=True)
    
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