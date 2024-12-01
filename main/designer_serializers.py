from rest_framework import serializers
from .models import ObjectName, PrimaryFiles, PrimaryDocuments


class ObjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectName
        fields = ['name']


