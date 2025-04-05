from rest_framework import generics, status 
from main.apps.common.pagination import CustomPagination
from main.apps.employee_communication.models import EmployeeCommunication
from . import serializers as employee_serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication





class BaseEmployeeCommunicationAPIView(generics.GenericAPIView):
    queryset = EmployeeCommunication.objects.all()
    serializer_class = employee_serializers.EmployeeCommunicationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



class EmployeeCommunicationCreateAPIView(BaseEmployeeCommunicationAPIView, generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "status_code": status.HTTP_201_CREATED,
                "message": "Employee Communication created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        return Response(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to create Employee Communication",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

employee_communication_create_api_view = EmployeeCommunicationCreateAPIView.as_view()



class EmployeeCommunicationListAPIView(BaseEmployeeCommunicationAPIView, generics.ListAPIView):

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
        queryset = EmployeeCommunication.objects.all()
        return queryset
    
    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator_class = self.get_pagination_class()

        if paginator_class:
            paginator = paginator_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", [])
            return response_data

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': "Employee Communication list successfully",
            "data": serializer.data,
            "status_code": status.HTTP_200_OK,
            }, 
            status=status.HTTP_200_OK)

employee_communication_list_api_view = EmployeeCommunicationListAPIView.as_view()



class EmployeeCommunicationDetailAPIView(BaseEmployeeCommunicationAPIView, generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                'message': "Employee Communication detail successfully",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

employee_communication_detail_api_view = EmployeeCommunicationDetailAPIView.as_view()



class EmployeeCommunicationUpdateAPIView(BaseEmployeeCommunicationAPIView, generics.UpdateAPIView):

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": "Employee Communication updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Failed to update Employee Communication",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

employee_communication_update_api_view = EmployeeCommunicationUpdateAPIView.as_view()



class EmployeeCommunicationDeleteAPIView(BaseEmployeeCommunicationAPIView, generics.DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "EmployeeCommunication deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )

employee_communication_delete_api_view = EmployeeCommunicationDeleteAPIView.as_view()

