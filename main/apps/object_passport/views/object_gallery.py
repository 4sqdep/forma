from main.apps.common.pagination import CustomPagination
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt import authentication
from rest_framework.parsers import MultiPartParser, FormParser
from main.apps.object_passport.models.object_gallery import Gallery
from main.apps.object_passport.serializers import object_gallery as object_gallery_serializer




class BaseGalleryAPIView(generics.GenericAPIView):
    queryset = Gallery.objects.all()
    serializer_class = object_gallery_serializer.ObjectGalleryCreateUpdateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

class ObjectGalleryCreateAPIView(BaseGalleryAPIView, generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
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



class ObjectGalleryUpdateAPIView(BaseGalleryAPIView, generics.UpdateAPIView):
    parser_classes = (MultiPartParser, FormParser)

    def update(self, request, *args, **kwargs):
        try:
            instance = Gallery.objects.get(pk=kwargs.get('pk'))
        except Gallery.DoesNotExist:
            return Response({
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Object Gallery not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status_code": status.HTTP_200_OK,
                "message": "Object Gallery updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "Failed to update Object Gallery",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

object_gallery_update_api_view = ObjectGalleryUpdateAPIView.as_view()



class ObjectGalleryListAPIView(BaseGalleryAPIView, generics.ListAPIView):

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Gallery.objects.filter(object_id=pk)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'message': "Rasmlar topilmadi",
                             'status_code': status.HTTP_404_NOT_FOUND,
                             'data': []}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status_code': status.HTTP_200_OK,
            'message': "Rasmlar Muvaffaqiyatli topildi",
            'data': serializer.data
        }, status=status.HTTP_200_OK)

object_gallery_list_api_view = ObjectGalleryListAPIView.as_view()



class ObjectGalleryDeleteAPIView(generics.DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "Object Gallery deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )

object_gallery_delete_api_view = ObjectGalleryDeleteAPIView.as_view()