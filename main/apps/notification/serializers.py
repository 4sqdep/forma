from rest_framework import serializers 
from django.utils.translation import gettext_lazy as _
from .models import Notification



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'employee',
            'manager',
            'resource_request',
            'message',
            'is_read'
        )


