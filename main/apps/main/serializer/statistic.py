from rest_framework import serializers
from main.apps.main.models import ObjectsPassword
from main.apps.dashboard.models.dashboard import (
    Object,
    ObjectCategory,
    ObjectSubCategory
)
from django.db.models import Sum, Count



class ObjectCategoryStatisticsSerializer(serializers.ModelSerializer):
    category_data = serializers.SerializerMethodField()
    total_category_count = serializers.SerializerMethodField()
    total_subcategory_count = serializers.SerializerMethodField()
    total_price_sum = serializers.SerializerMethodField()

    class Meta:
        model = ObjectCategory
        fields = [
            'id',
            'name',
            'category_data',
            'total_category_count',
            'total_subcategory_count',   
            'total_price_sum'
        ]

    def get_category_data(self, obj):
        category_data = (
            Object.objects.filter(object_category=obj)
            .values('object_subcategory')
            .annotate(
                total_price=Sum('total_price'),
                count=Count('object_subcategory')
            )
        )
        return [
            {
                "object_subcategory_id": data['object_subcategory'],  
                "object_subcategory_name": ObjectSubCategory.objects.get(id=data['object_subcategory']).name if data['object_subcategory'] else None,  
                "count": data['count'],  
                "total_price": data['total_price'] or 0  
            }
            for data in category_data
        ]

    def get_total_category_count(self, obj):
        return Object.objects.filter(object_category=obj).values('object_subcategory').distinct().count()

    def get_total_subcategory_count(self, obj):
        return Object.objects.filter(object_category=obj).values('object_subcategory').distinct().count()

    def get_total_price_sum(self, obj):
        return Object.objects.filter(object_category=obj).aggregate(total_sum=Sum('total_price'))['total_sum'] or 0

