from django.contrib import admin
from main.apps.construction_work.models.file import ConstructionInstallationFile
from main.apps.construction_work.models.fund import ConstructionInstallationProject, MonthlyCompletedTask
from main.apps.construction_work.models.section import ConstructionInstallationSection
from main.apps.construction_work.models.statistics import ConstructionInstallationStatistics
from main.apps.construction_work.models.work_volume import MonthlyWorkVolume, WorkCategory, WorkType, WorkVolume




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

class WorkVolumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_category', 'work_type', 'plan', 'fact']
    list_display_links = ['work_category', 'work_type', 'plan', 'fact']

admin.site.register(WorkType)
admin.site.register(WorkVolume, WorkVolumeAdmin)


class WorkCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'object', 'title']
    list_display_links = ['object', 'title']
    search_fields = ['title']

admin.site.register(WorkCategory, WorkCategoryAdmin)


class MonthlyWorkVolumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_volume', 'plan', 'fact', 'date']
    list_display_links = ['work_volume',]
    search_fields = ['plan']

admin.site.register(MonthlyWorkVolume, MonthlyWorkVolumeAdmin)
