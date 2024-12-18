from rest_framework import serializers 
from .models import Country, Region, District
import ast


class CountrySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Country
        fields = (
            'id',
            'name'
        )
    
    def get_name(self, obj):
        try:
            name_data = ast.literal_eval(obj.name)  
            return name_data
        except (ValueError, SyntaxError):
            return {"uz": obj.name, "ru": obj.name, "en": obj.name, "krl": obj.name}



class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    name = serializers.SerializerMethodField()
    class Meta:
        model = Region
        fields = (
            'id',
            'name',
            'country',
        )
    
    def get_name(self, obj):
        try:
            name_data = ast.literal_eval(obj.name)  
            return name_data
        except (ValueError, SyntaxError):
            return {"uz": obj.name, "ru": obj.name, "en": obj.name, "krl": obj.name}



class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    name = serializers.SerializerMethodField()
    class Meta:
        model = District
        fields = (
            'id',
            'name',
            'region'
        )
    
    def get_name(self, obj):
        try:
            name_data = ast.literal_eval(obj.name)  
            return name_data
        except (ValueError, SyntaxError):
            return {"uz": obj.name, "ru": obj.name, "en": obj.name, "krl": obj.name}




