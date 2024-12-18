from ...resource.models.material import Material, MaterialCategory
from rest_framework import serializers 




class MaterialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = (
            'id',
            'title',
        )


class MaterialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = (
            'material_category',
            'title',
            'measurement'
        )



class MaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = (
            'id',
            'material_category',
            'title',
            'measurement'
        )
