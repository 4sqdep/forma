from rest_framework import serializers
from main.apps.construction_work.models.work_volume import MonthlyWorkVolume, WorkCategory, WorkType




class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = (
            'id',
            'object',
            'title',
            'measurement'
        )



class WorkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkCategory
        fields = (
            'id',
            'object',
            'title'
        )



class MonthlyWorkVolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyWorkVolume
        fields = (
            'id',
            'work_category',
            'work_type',
            'plan',
            'fact',
            'date'
        )