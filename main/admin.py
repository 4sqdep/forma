from django.contrib import admin
from .models import Post, ObjectName, PrimaryFiles, PrimaryDocuments


class ObjectNameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_display_links = ['name']
    search_fields = ['name']


admin.site.register(ObjectName, ObjectNameAdmin)


class PrimaryFilesInline(admin.TabularInline):
    model = PrimaryFiles
    extra = 1
    fields = ['file']
    can_delete = True


class PrimaryDocumentsAdmin(admin.ModelAdmin):
    inlines = [PrimaryFilesInline]
    list_display = ['id', 'object_name', 'name', 'file_code', 'created_at']
    list_display_links = ['name', 'created_at']
    search_fields = ['name', 'file_code']

admin.site.register(PrimaryDocuments, PrimaryDocumentsAdmin)


admin.site.register(Post)