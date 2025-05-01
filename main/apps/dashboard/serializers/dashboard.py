from rest_framework import serializers
from main.apps.dashboard.models.dashboard import (
    ObjectCategory, 
    ObjectSubCategory
)
from main.apps.object_passport.models.object import Object
from django.db.models import Sum, Count




class ObjectCategorySerializer(serializers.ModelSerializer):
    category_count = serializers.IntegerField(read_only=True)
    has_data = serializers.BooleanField(read_only=True)
    class Meta:
        model = ObjectCategory
        fields = (
            'id', 
            'name', 
            'slug_name',
            'category_count', 
            'has_data'
        )



class ObjectSubCategorySerializer(serializers.ModelSerializer):
    object_category = ObjectCategorySerializer
    subcategory_count = serializers.IntegerField(read_only=True)
    has_data = serializers.BooleanField(read_only=True)
    class Meta:
        model = ObjectSubCategory
        fields = (
            'id', 
            'object_category', 
            'name', 
            'subcategory_count', 
            'has_data'
        )

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

        result = []
        for data in category_data:
            subcategory_id = data['object_subcategory']
            subcategory_title = ObjectSubCategory.objects.get(id=subcategory_id).name if subcategory_id else None

            # Ushbu subkategoriya ichidagi barcha obyektlarni olish
            related_objects = (
                Object.objects.filter(object_subcategory_id=subcategory_id).values(
                'id', 'title', 'total_price', 'currency__title', 'object_power', 'annual_electricity_production'
            ))

            result.append({
                "object_subcategory_id": subcategory_id,
                "object_subcategory_title": subcategory_title,
                "count": data['count'],
                "total_price": data['total_price'] or 0,
                "objects": [
                    {
                        "object_id": obj_data['id'],
                        "object_title": obj_data['title'],
                        "object_object_power": obj_data['object_power'],
                        "object_annual_electricity_production": obj_data['annual_electricity_production'],
                        "object_currency": obj_data['currency__title'],
                        "object_price": obj_data['total_price'] or 0
                    }
                    for obj_data in related_objects
                ]
            })

        return result

    def get_total_category_count(self, obj):
        return Object.objects.filter(object_category=obj).count()

    def get_total_subcategory_count(self, obj):
        return Object.objects.filter(object_category=obj).values('object_subcategory').distinct().count()

    def get_total_price_sum(self, obj):
        return Object.objects.filter(object_category=obj).aggregate(total_sum=Sum('total_price'))['total_sum'] or 0


# class ObjectCategoryStatisticsSerializer(serializers.ModelSerializer):
#     category_data = serializers.SerializerMethodField()
#     total_category_count = serializers.SerializerMethodField()
#     total_subcategory_count = serializers.SerializerMethodField()
#     total_price_sum = serializers.SerializerMethodField()
#
#     class Meta:
#         model = ObjectCategory
#         fields = [
#             'id',
#             'name',
#             'category_data',
#             'total_category_count',
#             'total_subcategory_count',
#             'total_price_sum'
#         ]
#
#     def get_category_data(self, obj):
#         category_data = (
#             Object.objects.filter(object_category=obj)
#             .values('object_subcategory')
#             .annotate(
#                 total_price=Sum('total_price'),
#                 count=Count('object_subcategory')
#             )
#         )
#         return [
#             {
#                 "object_subcategory_id": data['object_subcategory'],
#                 "object_subcategory_title": ObjectSubCategory.objects.get(id=data['object_subcategory']).name if data['object_subcategory'] else None,
#                 "count": data['count'],
#                 "total_price": data['total_price'] or 0
#             }
#             for data in category_data
#         ]
#
#     def get_total_category_count(self, obj):
#         return Object.objects.filter(object_category=obj).values('object_subcategory').distinct().count()
#
#     def get_total_subcategory_count(self, obj):
#         return Object.objects.filter(object_category=obj).values('object_subcategory').distinct().count()
#
#     def get_total_price_sum(self, obj):
#         return Object.objects.filter(object_category=obj).aggregate(total_sum=Sum('total_price'))['total_sum'] or 0

# class ObjectCreateUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Object
#         fields = (
#             'object_category',
#             'object_subcategory',
#             'currency',
#             'title',
#             'community_fund',
#             'foreign_loan',
#             'construction_work_amount',
#             'equipment_amount',
#             'other_expense',
#             'total_price',
#             'object_power',
#             'annual_electricity_production',
#             'pressure',
#             'water_consumption',
#             'object_file',
#             'useful_work_coefficient',
#             'latitude',
#             'longitude',
#             'start_date',
#             'end_date',
#         )


# class ObjectSerializer(serializers.ModelSerializer):
#     currency_slug = serializers.CharField(source='currency.slug_title', read_only=True)
#     class Meta:
#         model = Object
#         fields = (
#             'id',
#             'object_category',
#             'object_subcategory',
#             'currency',
#             'currency_slug',
#             'title',
#             'community_fund',
#             'foreign_loan',
#             'construction_work_amount',
#             'equipment_amount',
#             'other_expense',
#             'total_price',
#             'object_power',
#             'annual_electricity_production',
#             'pressure',
#             'water_consumption',
#             'object_file',
#             'useful_work_coefficient',
#             'latitude',
#             'longitude',
#             'start_date',
#             'end_date',
#         )




