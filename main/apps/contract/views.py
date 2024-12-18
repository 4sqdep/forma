from main.apps.common.response import DestroyResponse, ListResponse, PostResponse, PutResponse
from main.apps.contract.models import Contract
from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from . import serializers as contract_serializer
from ..common.pagination import CustomPagination



class ContractCreateAPIView(generics.CreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = contract_serializer.ContractCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            contract = serializer.save()
            return PostResponse(status_code=status.HTTP_201_CREATED, message=contract.id, data=serializer.data, status=status.HTTP_201_CREATED)
        return ListResponse(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

contract_create_api_view = ContractCreateAPIView.as_view()



class ContractListAPIView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = contract_serializer.ContractListSerializer
    pagination_class = CustomPagination
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.all()
        client_name = self.request.query_params.get('client_name')
        inn = self.request.query_params.get('inn')
        date = self.request.query_params.get('date')
        phone_number = self.request.query_params.get('phone_number')

        if client_name:
            queryset = queryset.filter(checklist__statement__full_name=client_name)

        if inn:
            queryset = queryset.filter(checklist__statement__inn=inn)

        if date:
            queryset = queryset.filter(date=date)
        
        if phone_number:
            queryset = queryset.filter(checklist__statement__phone_number=phone_number)
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

contract_list_api_view = ContractListAPIView.as_view()



class ContractDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return contract_serializer.ContractListSerializer
        return contract_serializer.ContractCreateSerializer

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

contract_detail_api_view = ContractDetailAPIView.as_view()