from rest_framework import serializers
from main.apps.common.serializers import MeasurementSerializer
from main.apps.construction_work.models.work_volume import MonthlyWorkVolume, WorkCategory, WorkType, WorkVolume
from django.db.models import Sum






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
        monthly_work_volume_plan = MonthlyWorkVolume.objects.filter(work_volume__work_type=obj).aggregate(Sum('plan'))['plan__sum'] or 0
        return float(work_volume_plan) + float(monthly_work_volume_plan)
    
    def get_fact(self, obj):
        work_volume_fact = WorkVolume.objects.filter(work_type=obj).aggregate(Sum('fact'))['fact__sum'] or 0
        monthly_work_volume_fact = MonthlyWorkVolume.objects.filter(work_volume__work_type=obj).aggregate(Sum('fact'))['fact__sum'] or 0
        return float(work_volume_fact) + float(monthly_work_volume_fact)

    # def get_completed_percent(self, obj):
    #     plan = self.get_plan(obj)
    #     fact = self.get_fact(obj)
    #     if plan == 0:
    #         return 0
    #     remain = plan - fact
    #     remain_percent = (remain / plan) * 100
    #     return round(remain_percent, 2)

    def get_remained_volume(self, obj):
        plan = self.get_plan(obj)
        fact = self.get_fact(obj)
        return plan - fact
    
    def get_completed_percent(self, obj):
        plan = self.get_plan(obj)
        fact = self.get_fact(obj)
        if plan is None or plan == 0:
            return 0.0
        completed_percent = (fact / plan) * 100
        return round(completed_percent, 2)

    
        


class WorkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkCategory
        fields = (
            'id',
            'object',
            'title'
        )



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
    
    def get_completed_percent(self, obj):
        plan = obj.plan
        fact = obj.fact
        if plan is None or plan == 0:
            return 0.0
        completed_percent = fact / plan * 100
        return round(completed_percent, 2)
    
    def get_remained_volume(self, obj):
        plan = obj.plan
        fact = obj.fact
        return plan - fact



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

        work_category = validated_data.get('work_category')
        work_type = validated_data.get('work_type')
        plan = validated_data.get('plan')
        fact = validated_data.get('fact')

        work_volume, created = WorkVolume.objects.get_or_create(
            work_category=work_category,
            work_type=work_type,
            defaults={'plan': 0, 'fact': 0}
        )

        work_volume.plan += plan
        work_volume.fact += fact
        work_volume.save()
        return monthly_volume



class MonthlyWorkVolumeSerializer(serializers.ModelSerializer):
    work_category = serializers.CharField(source='work_category.title')
    work_type = serializers.CharField(source='work_type.title')
    remained_volume = serializers.SerializerMethodField()
    completed_percent = serializers.SerializerMethodField()

    class Meta:
        model = MonthlyWorkVolume
        fields = (
            'id',
            'work_category',
            'work_type',
            'work_volume',
            'plan',
            'fact',
            'date',
            'remained_volume',
            'completed_percent'
        )
    
    def get_completed_percent(self, obj):
        plan = obj.plan
        fact = obj.fact
        if plan is None or plan == 0:
            return 0.0
        completed_percent = fact / plan * 100
        return round(completed_percent, 2)
    
    def get_remained_volume(self, obj):
        plan = obj.plan
        fact = obj.fact
        return plan - fact

