from rest_framework import serializers
from main.apps.role.models import Role






class RoleSerializer(serializers.ModelSerializer):
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