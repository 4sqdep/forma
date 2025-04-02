from main.apps.common.pagination import CustomPagination
from main.apps.dashboard.models.dashboard import (
    ObjectCategory, 
    ObjectSubCategory
)
from main.apps.dashboard.serializers.dashboard import (
    ObjectCategorySerializer,
    ObjectSubCategorySerializer
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
from django.utils.dateparse import parse_date




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
            return Response({"message": "Sub Category", "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": f"Xatolik yuz berdi: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = ObjectSubCategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({"message": "Sub Category", "data": serializer.data}, status=status.HTTP_201_CREATED)
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
            return Response({"message": "Sub Category List", "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": f"Xatolik yuz berdi: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

object_subcategory_list_api_view = ObjectSubCategoryListAPIView.as_view()

