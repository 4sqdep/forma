from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.equipment.models.industrial_equipment import EquipmentStatus, EquipmentSubCategory, IndustrialAsset, EquipmentCategory
from ..serializers import industrial_equipment as industrial_equipment_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Q



class EquipmentCategoryCreateAPIView(generics.CreateAPIView):
    queryset = EquipmentCategory.objects.all()
    serializer_class = industrial_equipment_serializer.EquipmentCategoryCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Industrial Equipment"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Failed to create Industrial Equipment", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

equipment_category_create_api_view = EquipmentCategoryCreateAPIView.as_view()



class EquipmentCategoryListAPIView(generics.ListAPIView):
    serializer_class = industrial_equipment_serializer.EquipmentCategoryListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        hydro_station_id = self.kwargs.get('hydro_station_id')
        search = self.request.query_params.get('search', None)

        query = """
            SELECT ie.*
            FROM equipment_category ie
            WHERE (%s IS NULL OR ie.hydro_station_id = %s)
            AND (%s IS NULL OR ie.title ILIKE %s);
        """
        search_param = f"%{search}%" if search else None
        return EquipmentCategory.objects.raw(query, [hydro_station_id, hydro_station_id, search_param, search_param])


    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator_class = self.get_pagination_class()

        if paginator_class:
            paginator = paginator_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", [])
            return response_data

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

equipment_category_list_api_view = EquipmentCategoryListAPIView.as_view()



class EquipmentCategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = EquipmentCategory.objects.all()
    serializer_class = industrial_equipment_serializer.EquipmentCategoryListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

equipment_category_detail_api_view = EquipmentCategoryDetailAPIView.as_view()


class EquipmentCategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = EquipmentCategory.objects.all()
    serializer_class = industrial_equipment_serializer.EquipmentCategoryCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Industrial Equipment", "status_code": status.HTTP_200_OK})
        return Response({"message": "Failed to update Industrial Equipment", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

equipment_category_update_api_view = EquipmentCategoryUpdateAPIView.as_view()



class EquipmentCategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = EquipmentCategory.objects.all()
    serializer_class = industrial_equipment_serializer.EquipmentCategoryListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Industrial Equipment", "status_code": status.HTTP_204_NO_CONTENT})

equipment_category_delete_api_view = EquipmentCategoryDeleteAPIView.as_view()



class EquipmentSubCategoryCreateAPIView(generics.CreateAPIView):
    queryset = EquipmentSubCategory.objects.all()
    serializer_class = industrial_equipment_serializer.EquipmentSubCategorySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Equipment Category"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Failed to create Equipment Category", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

equipment_subcategory_create_api_view = EquipmentSubCategoryCreateAPIView.as_view()



class EquipmentSubCategoryListAPIView(generics.ListAPIView):
    serializer_class = industrial_equipment_serializer.EquipmentSubCategorySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = EquipmentSubCategory.objects.all()
        equipment_category = self.kwargs.get('equipment_category')
        if equipment_category:
            queryset = queryset.filter(equipment_category=equipment_category)
        return queryset

    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator_class = self.get_pagination_class()

        if paginator_class:
            paginator = paginator_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", [])
            return response_data

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})

equipment_subcategory_list_api_view = EquipmentSubCategoryListAPIView.as_view()



class EquipmentSubCategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = EquipmentSubCategory.objects.all()
    serializer_class = industrial_equipment_serializer.EquipmentSubCategorySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

equipment_subcategory_detail_api_view = EquipmentSubCategoryDetailAPIView.as_view()


class EquipmentSubCategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = EquipmentSubCategory.objects.all()
    serializer_class = industrial_equipment_serializer.EquipmentSubCategorySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Equipment Subcategory"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Failed to update Equipment Subcategory", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

equipment_subcategory_update_api_view = EquipmentSubCategoryUpdateAPIView.as_view()



class EquipmentSubCategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = EquipmentSubCategory.objects.all()
    serializer_class = industrial_equipment_serializer.EquipmentSubCategorySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        equipment_cateogry = instance.equipment_category
        self.perform_destroy(instance)
        if equipment_cateogry and EquipmentSubCategory.objects.filter(equipment_cateogry=equipment_cateogry).exists():
            equipment_cateogry.has_subcategories = False
            equipment_cateogry.save()
        return Response({"message": "Equipment Subcategory successfully deleted!"}, status=status.HTTP_204_NO_CONTENT)

equipment_subcategory_delete_api_view = EquipmentSubCategoryDeleteAPIView.as_view()



class IndustrialAssetCreateAPIView(generics.CreateAPIView):
    queryset = IndustrialAsset.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialAssetCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Industrial Asset"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Failed to create Industrial Asset", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

industrial_asset_create_api_view = IndustrialAssetCreateAPIView.as_view()



class IndustrialAssetListAPIView(generics.ListAPIView):
    serializer_class = industrial_equipment_serializer.IndustrialAssetListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = IndustrialAsset.objects.select_related("equipment_category", "measurement")
        equipment_category = self.kwargs.get("equipment_category") 
        equipment_subcategory = self.kwargs.get("equipment_subcategory")  
        equipment_subcategory = self.request.query_params.get("equipment_subcategory")
        status_param = self.request.query_params.get("status")

        if equipment_category:
            category = EquipmentCategory.objects.filter(id=equipment_category).first()
            if category and category.has_subcategories and not equipment_subcategory:
                return IndustrialAsset.objects.none()

        filter_conditions = Q()
        if equipment_category:
            filter_conditions &= Q(equipment_category=equipment_category)
        if equipment_subcategory:
            filter_conditions &= Q(equipment_subcategory=equipment_subcategory)
        if status_param in [EquipmentStatus.CREATED, EquipmentStatus.IN_TRANSIT, EquipmentStatus.DELIVERED]:
            filter_conditions &= Q(status=status_param)
        queryset = queryset.filter(filter_conditions)
        return queryset

    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        paginator_class = self.get_pagination_class()
        if paginator_class:
            paginator = paginator_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", [])
            return response_data

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})

industrial_asset_list_api_view = IndustrialAssetListAPIView.as_view()



class IndustrialAssetDetailAPIView(generics.RetrieveAPIView):
    queryset = IndustrialAsset.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialAssetListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

industrial_asset_detail_api_view = IndustrialAssetDetailAPIView.as_view()



class IndustrialAssetUpdateAPIView(generics.UpdateAPIView):
    queryset = IndustrialAsset.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialAssetCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Industrial Asset", "status_code": status.HTTP_200_OK})
        return Response({"message": "Failed to update Industrial Asset", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

industrial_asset_update_api_view = IndustrialAssetUpdateAPIView.as_view()



class IndustrialAssetDeleteAPIView(generics.DestroyAPIView):
    queryset = IndustrialAsset.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialAssetListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Industrial Asset", "status_code": status.HTTP_204_NO_CONTENT})

industrial_asset_delete_api_view = IndustrialAssetDeleteAPIView.as_view()



class AllIndustrialAssetListAPIView(generics.ListAPIView):
    serializer_class = industrial_equipment_serializer.IndustrialAssetListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = IndustrialAsset.objects.select_related("equipment_category", "measurement")
        obj = self.kwargs.get('obj')
        if obj:
            queryset = queryset.filter(object=obj)
        return queryset

    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_amount_sum = queryset.aggregate(total_sum=Sum('total_amount'))['total_sum'] or 0

        paginator_class = self.get_pagination_class()
        if paginator_class:
            paginator = paginator_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", [])
            response_data.data['total_amount_sum'] = round(total_amount_sum, 2)
            return response_data

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "data": serializer.data,
            "total_amount_sum": round(total_amount_sum, 2)
            })

all_industrial_asset_list_api_view = AllIndustrialAssetListAPIView.as_view()