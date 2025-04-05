from rest_framework import serializers
from main.apps.object_passport.models.object_gallery import Gallery


class ObjectGalleryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('id', 'object', 'name', 'file')