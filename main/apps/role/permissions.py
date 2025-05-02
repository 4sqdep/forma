from rest_framework import permissions
from .models import Role







class RoleObjectPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        try:
            role = Role.objects.get(employee=request.user)

            if obj not in role.object.all():
                return False

            if request.method in permissions.SAFE_METHODS:
                return True

            if request.method == "POST":
                return role.can_create
            elif request.method in ("PUT", "PATCH"):
                return role.can_update
            elif request.method == "DELETE":
                return role.can_delete

        except Role.DoesNotExist:
            return False

        return False
