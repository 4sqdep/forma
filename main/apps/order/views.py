from main.apps.order.models import Order
from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.common.response import DestroyResponse, ListResponse, PostResponse, PutResponse
from . import serializers as order_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = order_serializer.OrderCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return PostResponse(status_code=status.HTTP_201_CREATED, message=order.id, data=serializer.data, status=status.HTTP_201_CREATED)
        return ListResponse(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

order_create_api_view = OrderCreateAPIView.as_view()


class OrderListAPIView(generics.ListAPIView):
    serializer_class = order_serializer.OrderListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'employee_name', openapi.IN_QUERY, description='Employee Name', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'order_id', openapi.IN_QUERY, description='Order Id', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'client_type', openapi.IN_QUERY, description='Client Type', type=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'phone_number', openapi.IN_QUERY, description='Client Phone Number', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'contract_number', openapi.IN_QUERY, description='Contract Number', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_INTEGER
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Order.objects.select_related('checklist').all()
        employee_name = self.request.query_params.get('employee_name')
        order_id = self.request.query_params.get('order_id')
        client_type = self.request.query_params.get('client_type')
        phone_number = self.request.query_params.get('phone_number')
        contact_phone_number = self.request.query_params.get('contract_number')

        if employee_name:
            queryset = queryset.filter(checklist__statement__get_full_name=employee_name)
        
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        
        if client_type:
            queryset = queryset.filter(checklist__statement__client_type=client_type)
        
        if phone_number:
            queryset = queryset.filter(checklist__statement__phone_number=phone_number)
        
        if contact_phone_number:
            queryset = queryset.filter(checklist__statement__contact_phone_number=contact_phone_number)
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

order_list_api_view = OrderListAPIView.as_view()



class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.select_related('checklist').all()
    serializer_class = order_serializer.OrderListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return order_serializer.OrderCreateSerializer
        return order_serializer.OrderListSerializer

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

order_detail_api_view = OrderDetailAPIView.as_view()



