from rest_framework import serializers
from main.apps.main.models import ObjectsPassword
from main.apps.dashboard.models.dashboard import (
    DashboardButton,
    DashboardCategoryButton,
    DashboardSubCategoryButton
)
from django.db.models import Sum, Count




class DashboardButtonStatisticsSerializer(serializers.ModelSerializer):
    category_data = serializers.SerializerMethodField()
    total_category_count = serializers.SerializerMethodField()
    total_subcategory_count = serializers.SerializerMethodField()
    total_price_sum = serializers.SerializerMethodField()

    class Meta:
        model = DashboardButton
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
            ObjectsPassword.objects.filter(main_btn=obj)
            .values('category_btn')
            .annotate(
                total_price=Sum('total_price'),
                count=Count('category_btn')
            )
        )
        return [
            {
                "category_btn_id": data['category_btn'],  
                "category_btn_name": DashboardCategoryButton.objects.get(id=data['category_btn']).name if data['category_btn'] else None,  
                "count": data['count'],  
                "total_price": data['total_price'] or 0  
            }
            for data in category_data
        ]

    def get_total_category_count(self, obj):
        return ObjectsPassword.objects.filter(main_btn=obj).values('category_btn').distinct().count()

    def get_total_subcategory_count(self, obj):
        return ObjectsPassword.objects.filter(main_btn=obj).values('subcategory_btn').distinct().count()

    def get_total_price_sum(self, obj):
        return ObjectsPassword.objects.filter(main_btn=obj).aggregate(total_sum=Sum('total_price'))['total_sum'] or 0

