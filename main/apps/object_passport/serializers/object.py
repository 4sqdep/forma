from rest_framework import serializers
from main.apps.object_passport.models.object import Object





class ObjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = (
            'object_category',
            'object_subcategory',
            'currency',
            'title',
            'community_fund',
            'foreign_loan',
            'construction_work_amount',
            'equipment_amount',
            'other_expense',
            'total_price',
            'object_power',
            'annual_electricity_production',
            'pressure',
            'water_consumption',
            'object_file',
            'useful_work_coefficient',
            'latitude',
            'longitude',
            'start_date',
            'end_date',
        )


class ObjectSerializer(serializers.ModelSerializer):
    currency_slug = serializers.CharField(source='currency.slug_title', read_only=True)
    start_date = serializers.DateField(format="%d-%m-%Y", read_only=True)
    end_date = serializers.DateField(format="%d-%m-%Y", read_only=True)
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = Object
        fields = (
            'id',
            'object_category',
            'object_subcategory',
            'currency',
            'currency_slug',
            'title',
            'community_fund',
            'foreign_loan',
            'construction_work_amount',
            'equipment_amount',
            'other_expense',
            'total_price',
            'object_power',
            'annual_electricity_production',
            'pressure',
            'water_consumption',
            'object_file',
            'file_name',
            'useful_work_coefficient',
            'latitude',
            'longitude',
            'start_date',
            'end_date',
        )
    
    def get_file_name(self, obj):
        from urllib.parse import unquote
        
        if obj.object_file:
            file_url = obj.object_file.url
            filename_encoded = file_url.split("/")[-1]
            filename = unquote(filename_encoded)
            return filename.replace(" ", "_")
        return None



class ObjectTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = ['id', 'title']
