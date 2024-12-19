from main.apps.common.response import DestroyResponse, ListResponse, PostResponse, PutResponse
from main.apps.warehouse.models.material_warehouse import MaterialWarehouse
from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from ..serializers import material_warehouse as material_warehouse_serializer
from ...common.pagination import CustomPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class MaterialWarehouseCreateAPIView(generics.CreateAPIView):
    queryset = MaterialWarehouse.objects.all()
    serializer_class = material_warehouse_serializer.MaterialWarehouseCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            material_warehouse = serializer.save()
            return PostResponse(status_code=status.HTTP_201_CREATED, message=material_warehouse.id, data=serializer.data, status=status.HTTP_201_CREATED)
        return ListResponse(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

material_warehouse_create_api_view = MaterialWarehouseCreateAPIView.as_view()



class MaterialWarehouseListAPIView(generics.ListAPIView):
    queryset = MaterialWarehouse.objects.all()
    serializer_class = material_warehouse_serializer.MaterialWarehouseListSerializer
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
        material_category = self.request.query_params.get('material_category')
        material = self.request.query_params.get('material')
        measurement = self.request.query_params.get('measurement')

        if measurement:
            queryset = queryset.filter(measurement__title=measurement)

        if material_category:
            queryset = queryset.filter(material_category__title=material_category)

        if material:
            queryset = queryset.filter(material__title=material)
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

material_warehouse_list_api_view = MaterialWarehouseListAPIView.as_view()



class MaterialWarehouseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MaterialWarehouse.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return material_warehouse_serializer.MaterialWarehouseListSerializer
        return material_warehouse_serializer.MaterialWarehouseUpdateSerializer

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

material_warehouse_detail_api_view = MaterialWarehouseDetailAPIView.as_view()