from django.contrib import admin
from main.apps.contract.models import ContractSection, ContractFile



class ContractSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'object', 'title']
    list_display_links = ['object', 'title']
    search_fields = ['object__title', 'title']

admin.site.register(ContractSection, ContractSectionAdmin)


class ContractFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'section', 'title', 'date', 'file_code']
    list_display_links = ['section', 'title', 'date', 'file_code']
    search_fields = ['section__title', 'title', 'date', 'file_code']

admin.site.register(ContractFile, ContractFileAdmin)