from rest_framework import serializers
from main.apps.reestr.models.currency import Currency



class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency 
        fields = (
            'id',
            'title'
        )
