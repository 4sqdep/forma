from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.equipment.models.industrial_equipment import EquipmentStatus, IndustrialAsset, IndustrialEquipment
from ..serializers import industrial_equipment as industrial_equipment_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ...common.response import (
    PostResponse, 
    ErrorResponse,
    PutResponse, 
    ListResponse, 
    DestroyResponse
)


class IndustrialEquipmentCreateAPIView(generics.CreateAPIView):
    queryset = IndustrialEquipment.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialEquipmentCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return PostResponse(data=serializer.data, message="Industrial Equipment")
        return ErrorResponse(message="Failed to create Industrial Equipment", errors=serializer.errors)

industrial_equipment_create_api_view = IndustrialEquipmentCreateAPIView.as_view()


class IndustrialEquipmentListAPIView(generics.ListAPIView):
    serializer_class = industrial_equipment_serializer.IndustrialEquipmentListSerializer
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
        query = """
            SELECT ie.*
            FROM equipment_industrialequipment ie
            WHERE (%s IS NULL OR ie.hydro_station_id = %s);
        """
        return IndustrialEquipment.objects.raw(query, [hydro_station_id, hydro_station_id])

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
        return ListResponse(data=serializer.data, status_code=status.HTTP_200_OK)

industrial_equipment_list_api_view = IndustrialEquipmentListAPIView.as_view()



class IndustrialEquipmentDetailAPIView(generics.RetrieveAPIView):
    queryset = IndustrialEquipment.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialEquipmentListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ListResponse(serializer.data, status_code=status.HTTP_200_OK)

industrial_equipment_detail_api_view = IndustrialEquipmentDetailAPIView.as_view()



class IndustrialEquipmentUpdateAPIView(generics.UpdateAPIView):
    queryset = IndustrialEquipment.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialEquipmentCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=serializer.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return PutResponse(data=serializer.data, message="Industrial Equipment", status_code=status.HTTP_200_OK)
        return ErrorResponse(message="Failed to update Industrial Equipment", errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

industrial_equipment_update_api_view = IndustrialEquipmentUpdateAPIView.as_view()
    


class IndustrialEquipmentDeleteAPIView(generics.DestroyAPIView):
    queryset = IndustrialEquipment.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialEquipmentListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DestroyResponse(message="Industrial Equipment", status_code=status.HTTP_204_NO_CONTENT)

industrial_equipment_delete_api_view = IndustrialEquipmentDeleteAPIView.as_view()



class IndustrialAssetCreateAPIView(generics.CreateAPIView):
    queryset = IndustrialAsset.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialAssetCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return PostResponse(data=serializer.data, message="Industrial Asset")
        return ErrorResponse(message="Failed to create Industrial Asset", errors=serializer.errors)

industrial_asset_create_api_view = IndustrialAssetCreateAPIView.as_view()



class IndustrialAssetListAPIView(generics.ListAPIView):
    serializer_class = industrial_equipment_serializer.IndustrialAssetListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = IndustrialAsset.objects.select_related("industrial_equipment", "measurement")
        industrial_equipment_id = self.kwargs.get('industrial_equipment_id')
        hydro_station_id = self.kwargs.get('hydro_station_id')
        status_param = self.request.query_params.get('status')

        if industrial_equipment_id and hydro_station_id:
            queryset = queryset.filter(
                industrial_equipment=industrial_equipment_id,
                industrial_equipment__hydro_station=hydro_station_id
                )
        if status_param in [EquipmentStatus.CREATED, EquipmentStatus.IN_TRANSIT, EquipmentStatus.DELIVERED]:
            queryset = queryset.filter(status=status_param)

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
        return ListResponse(data=serializer.data, status_code=status.HTTP_200_OK)

industrial_asset_list_api_view = IndustrialAssetListAPIView.as_view()



class IndustrialAssetDetailAPIView(generics.RetrieveAPIView):
    queryset = IndustrialAsset.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialAssetListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ListResponse(serializer.data, status_code=status.HTTP_200_OK)

industrial_asset_detail_api_view = IndustrialAssetDetailAPIView.as_view()



class IndustrialAssetUpdateAPIView(generics.UpdateAPIView):
    queryset = IndustrialAsset.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialAssetCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=serializer.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return PutResponse(data=serializer.data, message="Industrial Asset", status_code=status.HTTP_200_OK)
        return ErrorResponse(message="Failed to update Industrial Asset", errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

industrial_asset_update_api_view = IndustrialAssetUpdateAPIView.as_view()
    


class IndustrialAssetDeleteAPIView(generics.DestroyAPIView):
    queryset = IndustrialAsset.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialAssetListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DestroyResponse(message="Industrial Asset", status_code=status.HTTP_204_NO_CONTENT)

industrial_asset_delete_api_view = IndustrialAssetDeleteAPIView.as_view()