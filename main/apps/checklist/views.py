from main.apps.resource.models.equipment import Equipment
from main.apps.service.models import Service
from main.apps.warehouse.models.equipment_warehouse import EquipmentWarehouse
from ..checklist.models import CheckList
from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.common.response import DestroyResponse, ListResponse, PostResponse, PutResponse
from . import serializers as checklist_serializer
from decimal import Decimal, InvalidOperation
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class CheckListCreateAPIView(generics.CreateAPIView):
    queryset = CheckList.objects.all()
    serializer_class = checklist_serializer.CheckListCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            checklist = serializer.save()

            service_total_price = 0
            services = request.data.get('service', [])
            if services:
                service_qs = Service.objects.filter(id__in=services)
                service_total_price = sum(service.service_price for service in service_qs)
            checklist.service_total_price = service_total_price

            equipment_total_price = 0
            equipments = request.data.get('equipment', [])
            measurement = request.data.get('measurement')
            if equipments and measurement:
                equipment_warehouses = EquipmentWarehouse.objects.filter(
                    equipment__id__in=equipments,
                    measurement__id=measurement
                )
                for equipment_warehouse in equipment_warehouses:
                    price = equipment_warehouse.measurement_data.get(str(measurement), 0)
                    equipment_total_price += price

            checklist.equipment_total_price = equipment_total_price

            discount_percent = request.data.get('discount_percent')
            discount_sum = request.data.get('discount_sum')

            try:
                discount_percent = Decimal(discount_percent) if discount_percent else Decimal(0)
                discount_sum = Decimal(discount_sum) if discount_sum else Decimal(0)
            except (ValueError, InvalidOperation):
                return ListResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    data={"error": "Invalid discount_percent or discount_sum format"},
                )

            checklist.payment_from_client = equipment_total_price + service_total_price

            if discount_percent > 0:
                checklist.payment_from_client -= (checklist.payment_from_client * discount_percent) / Decimal(100)

            if discount_sum > 0:
                checklist.payment_from_client -= discount_sum

            checklist.save(update_fields=['service_total_price', 'equipment_total_price', 'payment_from_client'])

            return PostResponse(
                status_code=status.HTTP_201_CREATED,
                message=checklist.id,
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return ListResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            data=serializer.errors,
        )

checklist_create_api_view = CheckListCreateAPIView.as_view()



class CheckListListAPIView(generics.ListAPIView):
    serializer_class = checklist_serializer.CheckListSerializer
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
        queryset = CheckList.objects.select_related('statement').all()
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

checklist_list_api_view = CheckListListAPIView.as_view()



class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CheckList.objects.select_related('statement').all()
    serializer_class = checklist_serializer.CheckListSerializer
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

checklist_detail_api_view = CheckListDetailAPIView.as_view()


