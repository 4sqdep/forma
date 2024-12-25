import re
from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.common.response import DestroyResponse, ListResponse, PostResponse, PutResponse
from ..models.statement import Statement
from ..serializers import statement as statement_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class StatementCreateAPIView(generics.CreateAPIView):
    queryset = Statement.objects.all()
    serializer_class = statement_serializer.StatementCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            statement = serializer.save()
            return PostResponse(status_code=status.HTTP_201_CREATED, message=statement.id, data=serializer.data, status=status.HTTP_201_CREATED)
        return ListResponse(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

statement_create_api_view = StatementCreateAPIView.as_view()


class StatementListAPIView(generics.ListAPIView):
    serializer_class = statement_serializer.StatementListSerializer
    # pagination_class = CustomPagination
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'address', openapi.IN_QUERY, description='Address', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'full_name', openapi.IN_QUERY, description='Client Full Name', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'client_type', openapi.IN_QUERY, description='Client Type', type=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'inn', openapi.IN_QUERY, description='INN', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'phone_number', openapi.IN_QUERY, description='Client Phone Number', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'contact_phone_number', openapi.IN_QUERY, description='Contact Phone Number', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status', openapi.IN_QUERY, description='Status', type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        queryset = Statement.objects.select_related(
            'employee', 
            'country', 
            'region', 
            'district'
        )
        if not user.is_superuser:
            queryset = queryset.filter(employee=user.id)
        
        address = self.request.query_params.get('address')
        full_name = self.request.query_params.get('full_name')
        client_type = self.request.query_params.get('client_type')
        inn = self.request.query_params.get('inn')
        phone_number = self.request.query_params.get('phone_number')
        contact_phone_number = self.request.query_params.get('contact_phone_number')
        status = self.request.query_params.get('status')

        if full_name:
            queryset = queryset.filter(full_name=full_name)
        
        if client_type:
            queryset = queryset.filter(client_type=client_type)
        
        if inn:
            queryset = queryset.filter(inn=inn)
        
        if phone_number:
            normalized_phone = re.sub(r'\D', '', phone_number)
            queryset = queryset.filter(phone_number__icontains=normalized_phone)
        
        if contact_phone_number:
            normalized_phone = re.sub(r'\D', '', contact_phone_number)
            queryset = queryset.filter(contact_phone_number__icontains=normalized_phone)
        
        if address:
            queryset = queryset.filter(address=address)

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

statement_list_api_view = StatementListAPIView.as_view()



class StatementDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = statement_serializer.StatementSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Statement.objects.select_related(
            'employee', 
            'country', 
            'region', 
            'district'
        )
        if not user.is_superuser:
            queryset = queryset.filter(employee=user.id)
        return queryset


    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return statement_serializer.StatementCreateSerializer
        if self.request.method == 'GET':
            return statement_serializer.StatementListSerializer
        return statement_serializer.StatementSerializer

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

statement_detail_api_view = StatementDetailAPIView.as_view()
