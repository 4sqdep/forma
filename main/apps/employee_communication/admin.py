from django.contrib import admin
from main.apps.employee_communication.models import EmployeeCommunication, FileMessage, TextMessage



admin.site.register(EmployeeCommunication)
admin.site.register(FileMessage)
admin.site.register(TextMessage)