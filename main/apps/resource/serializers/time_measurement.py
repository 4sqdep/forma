from ...resource.models.time_measurement import TimeMeasurement
from rest_framework import serializers 




class TimeMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeMeasurement
        fields = (
            'id',
            'title',
        )

