from main.apps.common.pagination import CustomPagination
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt import authentication
from rest_framework.parsers import MultiPartParser, FormParser
from main.apps.object_passport.models.object_gallery import Gallery
from main.apps.object_passport.serializers import object_gallery as object_gallery_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GalleryBaseAPIView(generics.GenericAPIView):
    queryset = Gallery.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        return getattr(self, 'serializer_class', object_gallery_serializer.ObjectGalleryCreateUpdateSerializer())


class ObjectGalleryCreateAPIView(GalleryBaseAPIView, generics.CreateAPIView):
    serializer_class = object_gallery_serializer.ObjectGalleryCreateUpdateSerializer()
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status_code": status.HTTP_201_CREATED,
                "message": "Object Gallery created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "Failed to create Object Gallery",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

object_gallery_api_view = ObjectGalleryCreateAPIView.as_view()