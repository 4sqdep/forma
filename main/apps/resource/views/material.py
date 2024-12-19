from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from ..models.material import MaterialCategory, Material
from ..serializers import material as material_serializer
from main.apps.common.pagination import CustomPagination
from main.apps.common.response import DestroyResponse, ListResponse, PostResponse, PutResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class MaterialCategoryCreateAPIView(generics.CreateAPIView):
    queryset = MaterialCategory.objects.all()
    serializer_class =  material_serializer.MaterialCategorySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            material_category = serializer.save()
            return PostResponse(status_code=status.HTTP_201_CREATED, message=material_category.id, data=serializer.data, status=status.HTTP_201_CREATED)
        return ListResponse(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

material_category_create_api_view = MaterialCategoryCreateAPIView.as_view()



class MaterialCategoryListAPIView(generics.ListAPIView):
    serializer_class =  material_serializer.MaterialCategorySerializer
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
        queryset = MaterialCategory.objects.all()
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

material_category_list_api_view = MaterialCategoryListAPIView.as_view()



class MaterialCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MaterialCategory.objects.all()
    serializer_class =  material_serializer.MaterialCategorySerializer
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

material_category_detail_api_view = MaterialCategoryDetailAPIView.as_view()




class MaterialCreateAPIView(generics.CreateAPIView):
    queryset = Material.objects.all()
    serializer_class =  material_serializer.MaterialCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            material = serializer.save()
            return PostResponse(status_code=status.HTTP_201_CREATED, message=material.id, data=serializer.data, status=status.HTTP_201_CREATED)
        return ListResponse(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

material_create_api_view = MaterialCreateAPIView.as_view()



class MaterialListAPIView(generics.ListAPIView):
    serializer_class =  material_serializer.MaterialListSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_INTEGER
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Material.objects.all()
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

material_list_api_view = MaterialListAPIView.as_view()



class MaterialDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Material.objects.all()
    serializer_class =  material_serializer.MaterialListSerializer
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

material_detail_api_view = MaterialDetailAPIView.as_view()
