from django.contrib import admin
from .models import Nocapitelni


class NocapitelniAdmin(admin.ModelAdmin):
    list_display = ['id', 'file']
    list_display_links = ['id', 'file']

admin.site.register(Nocapitelni, NocapitelniAdmin)
