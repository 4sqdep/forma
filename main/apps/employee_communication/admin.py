from django.contrib import admin
from main.apps.employee_communication.models import EmployeeCommunication, FileMessage, TextMessage



class EmployeeCommunicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'obj', 'title']
    list_display_links= ['sender', 'obj', 'title']
    search_fields = ['title', 'obj__title']

admin.site.register(EmployeeCommunication, EmployeeCommunicationAdmin)


class FileMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee_communication', 'sender']
    list_display_links = ['employee_communication', 'sender']
    search_fields = ['employee_communication__title']

admin.site.register(FileMessage, FileMessageAdmin)


class TextMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee_communication', 'sender']
    list_display_links = ['employee_communication', 'sender']
    search_fields = ['employee_communication__title']

admin.site.register(TextMessage, TextMessageAdmin)