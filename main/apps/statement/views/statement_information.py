from main.apps.common.response import DestroyResponse, ListResponse, PostResponse, PutResponse
from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from ..models.statement_information import StatementInformation
from ..serializers import statement_information as statement_information_serializer
from ...common.pagination import CustomPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class StatementInformationCreateAPIView(generics.CreateAPIView):
    queryset = StatementInformation.objects.all()
    serializer_class = statement_information_serializer.StatementInformationCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            statement_information = serializer.save()
            return PostResponse(status_code=status.HTTP_201_CREATED, message=statement_information.id, data=serializer.data, status=status.HTTP_201_CREATED)
        return ListResponse(status_code=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

statement_information_create_api_view = StatementInformationCreateAPIView.as_view()



class StatementInformationListAPIView(generics.ListAPIView):
    queryset = StatementInformation.objects.all()
    serializer_class = statement_information_serializer.StatementInformationListSerializer
    pagination_class = CustomPagination
    authentication_classes = [authentication.JWTAuthentication]
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
            return self.queryset.all()
        
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

statement_information_list_api_view = StatementInformationListAPIView.as_view()



class StatementInformationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StatementInformation.objects.all()
    serializer_class = statement_information_serializer.StatementInformationCreateSerializer
    pagination_class = CustomPagination
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return statement_information_serializer.StatementInformationSerializer
        if self.request.method == 'GET':
            return statement_information_serializer.StatementInformationSerializer
        return statement_information_serializer.StatementInformationSerializer

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

statement_information_detail_api_view = StatementInformationDetailAPIView.as_view()