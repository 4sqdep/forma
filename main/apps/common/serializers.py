from rest_framework import serializers
from main.apps.common.models import Currency, Measurement



class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency 
        fields = (
            'id',
            'title'
        )



class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement 
        fields = (
            'id',
            'title'
        )
