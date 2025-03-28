from django.contrib import admin
from main.apps.dashboard.models.construction_installation_work import (
    ConstructionInstallationFile, 
    ConstructionInstallationSection, 
    ConstructionInstallationStatistics,
    ConstructionInstallationProject,
    MonthlyCompletedTask
)
from main.apps.dashboard.models.dashboard import ObjectCategory, ObjectSubCategory, Object
from main.apps.dashboard.models.document import DocumentFiles, NextStageDocuments, ProjectSections



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


class NextStageDocumentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by_full_name', 'object', 'name',
                    'is_file', 'is_forma', 'is_section']
    list_display_links = ['name']
    search_fields = ['name']


    def created_by_full_name(self, obj):
        if obj.created_by:  
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        return "No user assigned"


admin.site.register(NextStageDocuments, NextStageDocumentsAdmin)


class DocumentFilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'document', 'created_by', 'files']
    list_display_links = ['document', 'files']


admin.site.register(DocumentFiles)


class ProjectSectionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'next_stage_documents', 'created_by', 'name']
    list_display_links = ['name']
    search_fields = ['name']

admin.site.register(ProjectSections, ProjectSectionsAdmin)

class AdminConstructionInstallationFile(admin.ModelAdmin):
    list_display = ['id', 'section', 'title', 'date', 'file_code']
    list_display_links = ['section', 'title', 'date', 'file_code']
    search_fields = ['title', 'file_code']

admin.site.register(ConstructionInstallationFile, AdminConstructionInstallationFile)


class AdminConstructionInstallationProject(admin.ModelAdmin):
    list_display = ['id', 'section', 'title', 'currency', 'allocated_amount']
    list_display_links = ['section', 'title', 'currency', 'allocated_amount']
    search_fields = ['title']

admin.site.register(ConstructionInstallationProject, AdminConstructionInstallationProject)


class AdminConstructionInstallationSection(admin.ModelAdmin):
    list_display = ['id', 'object', 'title', 'is_forma', 'is_file']
    list_display_links = ['object', 'title', 'is_forma', 'is_file']
    search_fields = ['title']

admin.site.register(ConstructionInstallationSection, AdminConstructionInstallationSection)


class AdminConstructionInstallationStatistics(admin.ModelAdmin):
    list_display = ['id', 'object', 'contractor', 'installation_work_amount', 'remanied_work_amount', 'cost_of_performed_work', 'date']
    list_display_links = ['object', 'contractor', 'installation_work_amount', 'remanied_work_amount', 'cost_of_performed_work', 'date']
    search_fields = ['contractor']

admin.site.register(ConstructionInstallationStatistics, AdminConstructionInstallationStatistics)


class AdminMonthlyCompletedTask(admin.ModelAdmin):
    list_display = ['id', 'construction_installation_project', 'date', 'monthly_amount']
    list_display_links = ['construction_installation_project', 'date', 'monthly_amount']
    search_fields = ['date']

admin.site.register(MonthlyCompletedTask, AdminMonthlyCompletedTask)