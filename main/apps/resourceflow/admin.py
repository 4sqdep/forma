from django.contrib import admin
from .models import ResourceRequest, ResourceReturn


admin.site.register(ResourceRequest)
admin.site.register(ResourceReturn)