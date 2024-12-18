from main.apps.resourceflow.models import ResourceRequest, ResourceReturn, StatusChoices
from main.apps.warehouse.models.equipment_warehouse import EquipmentWarehouse
from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.common.response import DestroyResponse, ListResponse, PostResponse, PutResponse
from . import serializers as resourceflow_serializer
from django.utils import timezone


class ResourceRequestCreateAPIView(generics.CreateAPIView):
    queryset =ResourceRequest.objects.all()
    serializer_class = resourceflow_serializer.ResourceRequestCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            resource_request = serializer.save()
            # current_time = timezone.now()
            # if resource_request.created_at != resource_request.pickup_time:
                
            return PostResponse(status_code=status.HTTP_201_CREATED, message=resource_request.id, data=serializer.data, status=status.HTTP_201_CREATED)
        return ListResponse(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

resource_request_create_api_view =ResourceRequestCreateAPIView.as_view()



class ResourceRequestListAPIView(generics.ListAPIView):
    serializer_class = resourceflow_serializer.ResourceRequestListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = ResourceRequest.objects.all()
        status = self.request.query_params.get('status')
        created_at = self.request.query_params.get('created_at')
        sender = self.request.query_params.get('sender')
        receiver = self.request.query_params.get('receiver')

        if sender:
            queryset = queryset.filter(sender__first_name=sender)
        
        if receiver:
            queryset = queryset.filter(receiver__first_name=receiver)

        if created_at:
            queryset = queryset.filter(created_at__date=created_at)

        if status:
            queryset = queryset.filter(status=status)
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

resource_request_list_api_view = ResourceRequestListAPIView.as_view()



class ResourceRequestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResourceRequest.objects.all()
    serializer_class = resourceflow_serializer.ResourceRequestListSerializer
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
        if instance.status == StatusChoices.NEW:
            instance.status = StatusChoices.IN_PROGRESS
            instance.save()
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

            if instance.status == StatusChoices.RESOLVED:
                try:
                    equipment_warehouse = EquipmentWarehouse.objects.filter(
                        equipment_category=instance.equipment_category, 
                        equipment=instance.equipment
                    ).first()
                    if equipment_warehouse.status != 'in stock':
                        return ListResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        message=f"Equipment is not available. Current status: {equipment_warehouse.status}."
                    )
                    equipment_warehouse.status == 'in use'
                    equipment_warehouse.save()  

                    current_time = timezone.now()
                    if instance.created_at != instance.pickup_time:
                        equipment_warehouse.status = 'booked'
                        equipment_warehouse.save()

                except EquipmentWarehouse.DoesNotExist:
                    return ListResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="Equipment Warehouse does not exist."
                )
            return PutResponse(
                status_code=status.HTTP_200_OK, 
                message=f"Updated: {updated_instance.id}", 
                data=serializer.data
            )
        return ListResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            data=serializer.errors
        )

resource_request_detail_api_view = ResourceRequestDetailAPIView.as_view()



class ResourceReturnCreateAPIView(generics.CreateAPIView):
    queryset = ResourceReturn.objects.all()
    serializer_class = resourceflow_serializer.ResourceReturnCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            resource_return = serializer.save()
            return PostResponse(status_code=status.HTTP_201_CREATED, message=resource_return.id, data=serializer.data, status=status.HTTP_201_CREATED)
        return ListResponse(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

resource_return_create_api_view = ResourceReturnCreateAPIView.as_view()



class ResourceReturnListAPIView(generics.ListAPIView):
    serializer_class = resourceflow_serializer.ResourceReturnListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = ResourceReturn.objects.all()
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

resource_return_list_api_view = ResourceReturnListAPIView.as_view()



class ResourceReturnDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResourceReturn.objects.all()
    serializer_class = resourceflow_serializer.ResourceReturnListSerializer
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
            if updated_instance.status == 'resolved':
                equipment_warehouse = EquipmentWarehouse.objects.filter(
                    equipment_category=instance.equipment_category, 
                    equipment=instance.equipment
                ).first()
                equipment_warehouse.status = 'in stock'
                equipment_warehouse.save()
            return PutResponse(
                status_code=status.HTTP_200_OK, 
                message=f"Updated: {updated_instance.id}", 
                data=serializer.data
            )
        return ListResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            data=serializer.errors
        )

resource_return_detail_api_view = ResourceReturnDetailAPIView.as_view()

