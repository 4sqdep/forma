from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from ..models.equipment import Equipment, EquipmentCategory
from ..serializers import equipment as equipment_serializer
from main.apps.common.pagination import CustomPagination
from main.apps.common.response import DestroyResponse, ListResponse, PostResponse, PutResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class EquipmentCategoryCreateAPIView(generics.CreateAPIView):
    queryset = EquipmentCategory.objects.all()
    serializer_class =  equipment_serializer.EquipmentCategorySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            equipment_category = serializer.save()
            return PostResponse(status_code=status.HTTP_201_CREATED, message=equipment_category.id, data=serializer.data, status=status.HTTP_201_CREATED)
        return ListResponse(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

equipment_category_create_api_view = EquipmentCategoryCreateAPIView.as_view()



class EquipmentCategoryListAPIView(generics.ListAPIView):
    serializer_class =  equipment_serializer.EquipmentCategorySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_INTEGER
            ),
        ]
    )
    
    def get_queryset(self):
        queryset = EquipmentCategory.objects.all()
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

equipment_category_list_api_view = EquipmentCategoryListAPIView.as_view()



class EquipmentCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EquipmentCategory.objects.all()
    serializer_class =  equipment_serializer.EquipmentCategorySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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

equipment_category_detail_api_view = EquipmentCategoryDetailAPIView.as_view()




class EquipmentCreateAPIView(generics.CreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class =  equipment_serializer.EquipmentCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            equipment = serializer.save()
            return PostResponse(status_code=status.HTTP_201_CREATED, message=equipment.id, data=serializer.data, status=status.HTTP_201_CREATED)
        return ListResponse(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

equipment_create_api_view = EquipmentCreateAPIView.as_view()



class EquipmentListAPIView(generics.ListAPIView):
    serializer_class =  equipment_serializer.EquipmentListSerializer
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
        queryset = Equipment.objects.select_related(
            'equipment_category', 
            'measurement', 
            'time_measurement' 
            ).all()
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

equipment_list_api_view = EquipmentListAPIView.as_view()



class EquipmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipment.objects.select_related(
            'equipment_category', 
            'measurement', 
            'time_measurement' 
            ).all()
    serializer_class =  equipment_serializer.EquipmentListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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

equipment_detail_api_view = EquipmentDetailAPIView.as_view()
