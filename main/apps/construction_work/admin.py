from django.contrib import admin
from main.apps.construction_work.models.file import ConstructionInstallationFile
from main.apps.construction_work.models.fund import ConstructionInstallationProject, MonthlyCompletedTask
from main.apps.construction_work.models.section import ConstructionInstallationSection
from main.apps.construction_work.models.statistics import ConstructionInstallationStatistics




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