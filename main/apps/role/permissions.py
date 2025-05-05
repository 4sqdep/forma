from .models import Role
from rest_framework import permissions





    
class RolePermissionMixin:
    required_permission = None 
    object_type = None  

    construction_related_types = {
        'construction_installation_file',
        'construction_installation_project',
        'monthly_completed_task',
        'construction_installation_section',
        'construction_installation_statistics',
        'work_type',
        'work_category',
        'work_volume',
        'monthly_work_volume'
    }

    equipment_related_types = {
        'hydro_station',
        'equipment_category',
        'equipment_subcategory',
        'industrial_asset'
    }

    contract_related_types = {
        'contract',
        'contract_section',
        'contract_file'
    }

    project_document_related_types = {
        'project_document_type',
        'project_document_file',
        'project_section',
        'construction_task',
        'monthly_expense'
    }

    employee_communication_related_type = {
        'employee_communication',
    }

    def has_permission_for_object(self, user, instance=None):
        try:
            role = Role.objects.get(employee=user)
        except Role.DoesNotExist:
            return False, "You do not have a role assigned."

        if self.object_type in self.construction_related_types:
            if not role.has_construction_work:
                return False, "You do not have access to construction work."

        elif self.object_type in self.equipment_related_types:
            if not role.has_equipment:
                return False, "You do not have access to equipment."

        elif self.object_type in self.contract_related_types:
            if not role.has_contract:
                return False, "You do not have access to contracts."

        elif self.object_type in self.project_document_related_types:
            if not role.has_project_document:
                return False, "You do not have access to project documents."

        if self.required_permission and not getattr(role, self.required_permission, False):
            return False, f"You do not have permission to {self.required_permission.replace('can_', '')} objects."

        if instance and instance not in role.object.all():
            return False, f"You are not allowed to {self.required_permission.replace('can_', '')} this object."
        
        elif self.object_type in self.employee_communication_related_type:
            if not role.has_employee_communication:
                return False, "You do not have access to create employee communication."
        return True, role



class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
