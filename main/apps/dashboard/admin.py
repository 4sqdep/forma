from django.contrib import admin
from main.apps.dashboard.models.dashboard import ObjectCategory, ObjectSubCategory, Object
from main.apps.dashboard.models.document import Files, NextStageDocuments, ProjectDocumentation, ProjectSections



class ObjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug_name']
    list_display_links = ['name']
    search_fields = ['name']


admin.site.register(ObjectCategory, ObjectCategoryAdmin)


class ObjectSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'object_category', 'name']
    list_display_links = ['object_category', 'name']
    search_fields = ['name']


admin.site.register(ObjectSubCategory, ObjectSubCategoryAdmin)


class ObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'object_subcategory', 'title']
    list_display_links = ['title']
    search_fields = ['title']


admin.site.register(Object, ObjectAdmin)

@admin.register(ProjectDocumentation)
class ProjectDocumentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'subcategories_btn', 'name', 'order')


class NextStageDocumentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by_full_name', 'subcategories_btn', 'project_document', 'name',
                    'is_file', 'is_forma', 'is_section']
    list_display_links = ['project_document', 'name']
    search_fields = ['name', 'project_document']


    def created_by_full_name(self, obj):
        if obj.created_by:  
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        return "No user assigned"


admin.site.register(NextStageDocuments, NextStageDocumentsAdmin)


class FilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'document', 'project_section', 'created_by', 'files']
    list_display_links = ['document', 'files']


admin.site.register(Files, FilesAdmin)


class ProjectSectionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'next_stage_documents', 'created_by', 'name']
    list_display_links = ['name']
    search_fields = ['name']

admin.site.register(ProjectSections, ProjectSectionsAdmin)