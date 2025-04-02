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
        return Response({
            "message": "Asosiy buttonlar",
            "data": serializer.data},
            status=status.HTTP_200_OK)

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



class ObjectAPIView(APIView):
    # permission_classes = [IsAuthenticated]    

    def post(self, request):
        serializer = ObjectCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Object created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Xatolik yuz berdi", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
    # permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        queryset = Object.objects.all()
        sub_category = self.kwargs.get('sub_category')
        search = self.request.query_params.get('search')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        new = self.request.query_params.get('new')
        old = self.request.query_params.get('old')
        expensive = self.request.query_params.get('expensive')
        cheap = self.request.query_params.get('cheap')
        high_energy = self.request.query_params.get('high_energy')
        low_energy = self.request.query_params.get('low_energy')

        if sub_category:
            queryset = queryset.filter(object_subcategory=sub_category)
        if search:
            queryset = queryset.filter(title__icontains=search)

        if start_date and end_date:
            queryset = queryset.filter(start_date__gte=start_date, end_date__lte=end_date)
        elif start_date and not end_date:
            queryset = queryset.filter(start_date=start_date)
        elif end_date and not start_date:
            queryset = queryset.filter(end_date=end_date)
        
        if new and new.lower() == 'true':
            queryset = queryset.order_by('-created_at')

        if old and old.lower() == 'true':
            queryset = queryset.order_by('created_at')
        
        if expensive and expensive.lower() == 'true':
            queryset = queryset.order_by('-total_price')  

        if cheap and cheap.lower() == 'true':
            queryset = queryset.order_by('total_price')  

        if high_energy and high_energy.lower() == 'true':
            queryset = queryset.order_by('-object_power')  

        if low_energy and low_energy.lower() == 'true':
            queryset = queryset.order_by('object_power')

        return queryset

    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.get_pagination_class()

        if paginator:
            paginator = paginator()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", None)
            return Response({'data': response_data.data}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "message": "Obyekt listlari...",
                "data": serializer.data},
                status=status.HTTP_200_OK)

object_list_api_view = ObjectListAPIView.as_view()



class ObjectDetailAPIView(generics.RetrieveAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "message": "Successfully",
            "data": serializer.data},
            status=status.HTTP_200_OK)

object_retrieve_api_view = ObjectDetailAPIView.as_view()
