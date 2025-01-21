from rest_framework import serializers
from main.apps.reestr.models.time_period import Month, Year




class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year 
        fields = (
            'id',
            'title'
        )


class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month
        fields = (
            'id',
            'year',
            'title',
        )

