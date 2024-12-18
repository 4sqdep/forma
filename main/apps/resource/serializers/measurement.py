from ...resource.models.measurement import Measurement
from rest_framework import serializers 



class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = (
            'title',
            'short_title'
        )



