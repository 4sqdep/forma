from main.apps.common.response import DestroyResponse, ListResponse, PostResponse, PutResponse
from main.apps.warehouse.models.equipment_warehouse import EquipmentWarehouse
from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from ..serializers import equipment_warehouse as equipment_warehouse_serializer
from ...common.pagination import CustomPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class EquipmentWarehouseCreateAPIView(generics.CreateAPIView):
    queryset = EquipmentWarehouse.objects.all()
    serializer_class = equipment_warehouse_serializer.EquipmentWarehouseCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            equipment_warehouse = serializer.save()
            return PostResponse(status_code=status.HTTP_201_CREATED, message=equipment_warehouse.id, data=serializer.data, status=status.HTTP_201_CREATED)
        return ListResponse(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

equipment_warehouse_create_api_view = EquipmentWarehouseCreateAPIView.as_view()



class EquipmentWarehouseListAPIView(generics.ListAPIView):
    queryset = EquipmentWarehouse.objects.all()
    serializer_class = equipment_warehouse_serializer.EquipmentWarehouseListSerializer
    pagination_class = CustomPagination
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'equipment_category', openapi.IN_QUERY, description='Equipment Category', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'equipment', openapi.IN_QUERY, description='Equipment', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'measurement', openapi.IN_QUERY, description='Measurement', type=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_INTEGER
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.all()
        equipment_category = self.request.query_params.get('equipment_category')
        equipment = self.request.query_params.get('equipment')
        measurement = self.request.query_params.get('measurement')

        if measurement:
            queryset = queryset.filter(measurement__title=measurement)

        if equipment_category:
            queryset = queryset.filter(equipment_category__title=equipment_category)
            
        if equipment:
            queryset = queryset.filter(equipment__title=equipment)
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
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data = ListResponse(status_code=status.HTTP_200_OK, data=serializer.data)
        return response_data

equipment_warehouse_list_api_view = EquipmentWarehouseListAPIView.as_view()



class EquipmentWarehouseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EquipmentWarehouse.objects.all()
    serializer_class = equipment_warehouse_serializer.EquipmentWarehouseCreateSerializer
    pagination_class = CustomPagination
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return equipment_warehouse_serializer.EquipmentWarehouseListSerializer
        return equipment_warehouse_serializer.EquipmentWarehouseCreateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DestroyResponse(
            status_code=status.HTTP_204_NO_CONTENT, 
            message=f"Deleted: {instance.id}"
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ListResponse(
            status_code=status.HTTP_200_OK, 
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return PutResponse(
                status_code=status.HTTP_200_OK, 
                message=f"Updated: {updated_instance.id}", 
                data=serializer.data
            )
        return ListResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            data=serializer.errors
        )

equipment_warehouse_detail_api_view = EquipmentWarehouseDetailAPIView.as_view()