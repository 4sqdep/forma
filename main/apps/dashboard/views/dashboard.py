from main.apps.dashboard.models.dashboard import (
    ObjectCategory, 
    ObjectSubCategory, 
    Object
)
from main.apps.dashboard.serializers.dashboard import (
    ObjectCategorySerializer,
    ObjectCreateUpdateSerializer, 
    ObjectSubCategorySerializer, 
    ObjectSerializer
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Case, When, Value, BooleanField
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics, status




class ObjectCategoryAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        object_category = ObjectCategory.objects.annotate(
            category_count=Count('objectsubcategory'),
            has_data=Case(
                When(category_count__gt=0, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        serializer = ObjectCategorySerializer(object_category, many=True)
        return Response({"message": "Asosiy buttonlar", "data": serializer.data}, status=status.HTTP_200_OK)

object_category_api_view = ObjectCategoryAPIView.as_view()


class ObjectSubCategoryAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            btns = (
                ObjectSubCategory.objects.filter(id=pk)
                .select_related('object_category')
                .annotate(
                    subcategory_count=Count('object_category', distinct=True),
                    has_data=Case(
                        When(subcategory_count__gt=0, then=Value(True)),
                        default=Value(False),
                        output_field=BooleanField()
                    )
                )
            )

            serializer = ObjectSubCategorySerializer(btns, many=True)
            return Response({"message": "Kategoriya buttonlar", "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": f"Xatolik yuz berdi: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = ObjectSubCategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({"message": "SubCategory", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Xatolik yuz berdi", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        obj = get_object_or_404(ObjectSubCategory, id=pk)
        serializer = ObjectSubCategorySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "SubCategory updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Xatolik yuz berdi", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        obj = get_object_or_404(ObjectSubCategory, id=pk)
        obj.delete()
        return Response({"message": "SubCategory deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

object_subcategory_api_view = ObjectSubCategoryAPIView.as_view()


class ObjectSubCategoryListAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            btns = (
                ObjectSubCategory.objects.filter(object_category_id=pk)
                .select_related('object_category')
                .annotate(
                    subcategory_count=Count('object_category', distinct=True),
                    has_data=Case(
                        When(subcategory_count__gt=0, then=Value(True)),
                        default=Value(False),
                        output_field=BooleanField()
                    )
                )
            )

            serializer = ObjectSubCategorySerializer(btns, many=True)
            return Response({"message": "Kategoriya buttonlar", "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": f"Xatolik yuz berdi: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

object_subcategory_list_api_view = ObjectSubCategoryListAPIView.as_view()



class ObjectAPIView(APIView):
    # permission_classes = [IsAuthenticated]    

    def post(self, request):
        serializer = ObjectCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Object created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Xatolik yuz berdi", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            obj = get_object_or_404(Object, id=pk)
            serializer = ObjectSerializer(obj)
            return Response({"message": "SubCategory buttonlar", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            objects = Object.objects.filter(object_subcategory_id=pk).select_related('object_subcategory')
            serializer = ObjectSerializer(objects, many=True)
            return Response({"message": "SubCategory buttonlar", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        obj = get_object_or_404(Object, id=pk)
        serializer = ObjectCreateUpdateSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Object updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Xatolik yuz berdi", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        obj = get_object_or_404(Object, id=pk)
        obj.delete()
        return Response({"message": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

object_api_view = ObjectAPIView.as_view()



class ObjectListAPIView(generics.ListAPIView):
    serializer_class = ObjectSerializer

    def get_queryset(self):
        """Filter objects by sub_category from URL kwargs"""
        sub_category = self.kwargs.get('sub_category')
        return Object.objects.filter(object_subcategory=sub_category)

    def list(self, request, *args, **kwargs):
        """Override list() to customize response format"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "data": serializer.data
        }, status=status.HTTP_200_OK)

object_list_api_view = ObjectListAPIView.as_view()