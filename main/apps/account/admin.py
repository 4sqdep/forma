from django.contrib import admin
from .models import User, ActivationSMSCode


admin.site.register(User)
admin.site.register(ActivationSMSCode)