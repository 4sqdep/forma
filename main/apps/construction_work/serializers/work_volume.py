from rest_framework import serializers
from django.db.models import Sum
from main.apps.construction_work.models.work_volume import (
    MonthlyWorkVolume, 
    WorkCategory, 
    WorkType, 
    WorkVolume
)
from main.apps.common.serializers import MeasurementSerializer





def calculate_percentage(fact, plan):
    if not plan:
        return 0
    return int(round((fact / plan) * 100, 2))


def calculate_remained(plan, fact):
    return plan - fact



class WorkTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = (
            'id',
            'object',
            'title',
            'measurement'
        )



class BaseWorkTypeSerializer(serializers.ModelSerializer):
    measurement = MeasurementSerializer()
    class Meta:
        model = WorkType
        fields = (
            'id',
            'object',
            'title',
            'measurement',
        )



class WorkTypeSerializer(serializers.ModelSerializer):
    plan = serializers.SerializerMethodField()
    fact = serializers.SerializerMethodField()
    completed_percent = serializers.SerializerMethodField()
    remained_volume = serializers.SerializerMethodField()
    measurement = MeasurementSerializer()

    class Meta:
        model = WorkType
        fields = (
            'id',
            'object',
            'title',
            'measurement',
            'plan',
            'fact',
            'remained_volume',
            'completed_percent'
        )
    
    def get_plan(self, obj):
        work_volume_plan = WorkVolume.objects.filter(work_type=obj).aggregate(Sum('plan'))['plan__sum'] or 0
        # monthly_work_volume_plan = MonthlyWorkVolume.objects.filter(work_volume__work_type=obj).aggregate(Sum('plan'))['plan__sum'] or 0
        return float(work_volume_plan) 
    
    def get_fact(self, obj):
        work_volume_fact = WorkVolume.objects.filter(work_type=obj).aggregate(Sum('fact'))['fact__sum'] or 0
        # monthly_work_volume_fact = MonthlyWorkVolume.objects.filter(work_volume__work_type=obj).aggregate(Sum('fact'))['fact__sum'] or 0
        return float(work_volume_fact)

    def get_remained_volume(self, obj):
        return calculate_remained(self.get_plan(obj), self.get_fact(obj))
    
    def get_completed_percent(self, obj):
        return calculate_percentage(self.get_fact(obj), self.get_plan(obj))



class WorkCategorySerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source='object.currency.title', required=False)
    completed_percent = serializers.SerializerMethodField(required=False)
    remained_amount = serializers.SerializerMethodField(required=False)
    
    class Meta:
        model = WorkCategory
        fields = (
            'id',
            'object',
            'title',
            'plan_amount',
            'fact_amount',
            'currency',
            'remained_amount',
            'completed_percent'
        )
    
    def get_remained_amount(self, obj):
        return calculate_remained(obj.plan_amount, obj.fact_amount)
    
    def get_completed_percent(self, obj):
        return calculate_percentage(obj.fact_amount, obj.plan_amount)



class WorkVolumeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkVolume
        fields = (
            'id',
            'work_category',
            'work_type',
            'plan',
            'fact'
        )



class WorkVolumeSerializer(serializers.ModelSerializer):
    work_category = WorkCategorySerializer()
    work_type = BaseWorkTypeSerializer()
    remained_volume = serializers.SerializerMethodField()
    completed_percent = serializers.SerializerMethodField()

    class Meta:
        model = WorkVolume
        fields = (
            'id',
            'work_category',
            'work_type',
            'plan',
            'fact',
            'remained_volume',
            'completed_percent'
        )

    def get_remained_volume(self, obj):
        return calculate_remained(obj.plan, obj.fact)
    
    def get_completed_percent(self, obj):
        return calculate_percentage(obj.fact, obj.plan)
    


class MonthlyWorkVolumeCreateSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y", input_formats=["%Y-%m-%d"], required=False)
    class Meta:
        model = MonthlyWorkVolume
        fields = (
            'id',
            'work_volume',
            'plan',
            'fact',
            'date'
        )
    
    def create(self, validated_data):
        monthly_volume = MonthlyWorkVolume.objects.create(**validated_data)

        work_volume = validated_data.get('work_volume')
        plan = validated_data.get('plan', 0)
        fact = validated_data.get('fact', 0)

        work_volume.plan += plan
        work_volume.fact += fact
        work_volume.save()
        return monthly_volume



class MonthlyWorkVolumeSerializer(serializers.ModelSerializer):
    work_category = serializers.CharField(source='work_category.title')
    work_type = serializers.CharField(source='work_type.title')
    remained_volume = serializers.SerializerMethodField()
    completed_percent = serializers.SerializerMethodField()
    measurement = serializers.CharField(source='work_volume.work_type.measurement.title')
    date = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = MonthlyWorkVolume
        fields = (
            'id',
            'work_category',
            'work_type',
            'work_volume',
            'measurement',
            'plan',
            'fact',
            'date',
            'remained_volume',
            'completed_percent'
        )
    
    def get_remained_volume(self, obj):
        return calculate_remained(obj.plan, obj.fact)

    def get_completed_percent(self, obj):
        return calculate_percentage(obj.fact, obj.plan)

