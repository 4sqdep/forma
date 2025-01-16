from django.contrib import admin

from main.apps.account.models.department import Department
from main.apps.account.models.position import Position
from main.apps.account.models.user import User, UserProfile


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'created_at']
    list_display_links = ['id', 'username', 'first_name', 'last_name']
    search_fields = ['username', 'first_name']


admin.site.register(User, UserAdmin)


class PositionAdminInline(admin.TabularInline):
    model = Position
    extra = 1
    fields = ['id', 'name', 'created_at']
    readonly_fields = ['created_at']
    can_delete = True


class DepartmentAdmin(admin.ModelAdmin):
    inlines = [PositionAdminInline]
    list_display = ['id', 'name', 'created_at']
    list_display_links = ['id', 'name']
    search_fields = ['name']


admin.site.register(Department, DepartmentAdmin)


# class PermissionAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'position', 'can_get', 'can_post', 'can_patch', 'can_put', 'can_delete', 'created_at']
#     list_display_links = ['id', 'position', 'can_get']
#     search_fields = ['position']


# admin.site.register(Permission, PermissionAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'department', 'position', 'created_at']
    list_display_links = ['id', 'user', 'department', 'position']
    search_fields = ['department']


admin.site.register(UserProfile, UserProfileAdmin)