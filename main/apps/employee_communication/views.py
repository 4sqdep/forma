from rest_framework import generics, status 
from main.apps.common.pagination import CustomPagination
from main.apps.employee_communication.filters import EmployeeCommunicationFilter
from main.apps.employee_communication.models import EmployeeCommunication, FileMessage, ProblemStatus, TextMessage
from . import serializers as employee_serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView


class BaseEmployeeCommunicationAPIView(generics.GenericAPIView):
    queryset = EmployeeCommunication.objects.select_related("sender").prefetch_related("employee")
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class EmployeeCommunicationCreateAPIView(BaseEmployeeCommunicationAPIView, generics.CreateAPIView):
    serializer_class = employee_serializers.EmployeeCommunicationCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=self.request.user)
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
    serializer_class = employee_serializers.EmployeeCommunicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeCommunicationFilter

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('p', openapi.IN_QUERY, description='Enable Pagination', type=openapi.TYPE_STRING),
        openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ])
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        object = self.kwargs.get('object')
        return queryset.filter(
            obj=object
            ).filter(
            Q(employee=self.request.user) | Q(sender=self.request.user)
        ).distinct()
    
    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator_class = self.get_pagination_class()

        counts = {
            "all": queryset.count(),
            "new": queryset.filter(status=ProblemStatus.NEW).count(),
            "done": queryset.filter(status=ProblemStatus.DONE).count(),
            "in_confirmation": queryset.filter(status=ProblemStatus.IN_CORFIRMATION).count(),
            "in_progress": queryset.filter(status=ProblemStatus.IN_PROGRESS).count(),
            "incomplete": queryset.filter(status=ProblemStatus.INCOMPLETE).count(),
            "completed_late": queryset.filter(status=ProblemStatus.COMPLETED_LATE).count(),
        }

        if paginator_class:
            paginator = paginator_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", [])
            response_data.data['counts'] = counts
            return response_data

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status_code": status.HTTP_200_OK,
            'message': "Employee Communication list successfully",
            "data": serializer.data,
            "counts": counts
            }, 
            status=status.HTTP_200_OK
            )

employee_communication_list_api_view = EmployeeCommunicationListAPIView.as_view()



class EmployeeCommunicationDetailAPIView(BaseEmployeeCommunicationAPIView, generics.RetrieveAPIView):
    serializer_class = employee_serializers.EmployeeCommunicationSerializer

    def get_queryset(self):
        return EmployeeCommunication.objects.select_related("sender").filter(
            Q(employee=self.request.user) | Q(sender=self.request.user)
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if instance.employee.filter(id=user.id).exists():
            if not instance.is_read:
                instance.is_read = True
                instance.read_time = now()
            instance.view_count += 1
            instance.save(update_fields=['is_read', 'read_time', 'view_count'])
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
    serializer_class = employee_serializers.EmployeeCommunicationCreateSerializer

    def get_queryset(self):
        return EmployeeCommunication.objects.select_related("sender").filter(
            Q(employee=self.request.user) | Q(sender=self.request.user)
        )

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
    serializer_class = employee_serializers.EmployeeCommunicationSerializer

    def get_queryset(self):
        return EmployeeCommunication.objects.select_related("sender").filter(
            Q(employee=self.request.user) | Q(sender=self.request.user)
        )

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




class AllEmployeeCommunicationListAPIView(BaseEmployeeCommunicationAPIView, generics.ListAPIView):
    serializer_class = employee_serializers.EmployeeCommunicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeCommunicationFilter

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('p', openapi.IN_QUERY, description='Enable Pagination', type=openapi.TYPE_STRING),
        openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ])
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(employee=self.request.user) | Q(sender=self.request.user)
        ).distinct()
    
    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator_class = self.get_pagination_class()

        counts = {
            "all": queryset.count(),
            "new": queryset.filter(status=ProblemStatus.NEW).count(),
            "done": queryset.filter(status=ProblemStatus.DONE).count(),
            "in_confirmation": queryset.filter(status=ProblemStatus.IN_CORFIRMATION).count(),
            "in_progress": queryset.filter(status=ProblemStatus.IN_PROGRESS).count(),
            "incomplete": queryset.filter(status=ProblemStatus.INCOMPLETE).count(),
            "completed_late": queryset.filter(status=ProblemStatus.COMPLETED_LATE).count(),
        }

        if paginator_class:
            paginator = paginator_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", [])
            response_data.data['counts'] = counts
            return response_data

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status_code": status.HTTP_200_OK,
            'message': "Employee Communication list successfully",
            "data": serializer.data,
            "counts": counts
            }, 
            status=status.HTTP_200_OK
            )

all_employee_communication_list_api_view = AllEmployeeCommunicationListAPIView.as_view()



class BaseFileMessageAPIView(generics.GenericAPIView):
    queryset = FileMessage.objects.all()
    serializer_class = employee_serializers.FileMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class FileMessageCreateAPIView(BaseFileMessageAPIView, generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=self.request.user)
            return Response(
            {
                "status_code": status.HTTP_201_CREATED,
                "message": "File Message created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        return Response(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to create File Message",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

file_message_create_api_view = FileMessageCreateAPIView.as_view()



class FileMessageListAPIView(BaseFileMessageAPIView, generics.ListAPIView):

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
        employee_communication = self.kwargs.get('employee_communication')
        queryset = FileMessage.objects.filter(
            Q(employee_communication=employee_communication) &
            Q(sender=self.request.user) |
            Q(receiver=self.request.user) 
        )
        model_name = self.request.query_params.get('model')
        if model_name:
            queryset = queryset.filter(content_type__model=model_name.lower())
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
            'message': "File Message list successfully",
            "data": serializer.data,
            "status_code": status.HTTP_200_OK,
            }, 
            status=status.HTTP_200_OK)

file_message_list_api_view = FileMessageListAPIView.as_view()



class FileMessageDetailAPIView(BaseFileMessageAPIView, generics.RetrieveAPIView):

    def get_queryset(self):
        return FileMessage.objects.filter(
            Q(sender=self.request.user) |
            Q(receiver=self.request.user) 
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if instance.receiver == user:
            if not instance.is_read:
                instance.is_read = True
                instance.read_time = now()
            instance.save(update_fields=['is_read', 'read_time'])
        serializer = self.get_serializer(instance)
        return Response(
            {
                'message': "File Message detail successfully",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

file_message_detail_api_view = FileMessageDetailAPIView.as_view()



class FileMessageUpdateAPIView(BaseFileMessageAPIView, generics.UpdateAPIView):

    def get_queryset(self):
        return FileMessage.objects.filter(
            Q(sender=self.request.user) |
            Q(receiver=self.request.user) 
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": "File Message updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Failed to update File Message",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

file_message_update_api_view = FileMessageUpdateAPIView.as_view()



class FileMessageDeleteAPIView(BaseFileMessageAPIView, generics.DestroyAPIView):

    def get_queryset(self):
        return FileMessage.objects.filter(
            Q(sender=self.request.user) |
            Q(receiver=self.request.user) 
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "File Message deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )

file_message_delete_api_view = FileMessageDeleteAPIView.as_view()



class BaseTextMessageAPIView(generics.GenericAPIView):
    queryset = TextMessage.objects.all()
    serializer_class = employee_serializers.TextMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



class TextMessageCreateAPIView(BaseTextMessageAPIView, generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=self.request.user)
            return Response(
            {
                "status_code": status.HTTP_201_CREATED,
                "message": "Text Message created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        return Response(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to create Text Message",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

text_message_create_api_view = TextMessageCreateAPIView.as_view()



class TextMessageListAPIView(BaseTextMessageAPIView, generics.ListAPIView):

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
        employee_communication = self.kwargs.get('employee_communication')
        queryset = TextMessage.objects.filter(
            Q(employee_communication=employee_communication) &
            Q(sender=self.request.user) |
            Q(receiver=self.request.user) 
        )
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
            'message': "Text Message list successfully",
            "data": serializer.data,
            "status_code": status.HTTP_200_OK,
            }, 
            status=status.HTTP_200_OK)

text_message_list_api_view = TextMessageListAPIView.as_view()



class TextMessageDetailAPIView(BaseTextMessageAPIView, generics.RetrieveAPIView):

    def get_queryset(self):
        return TextMessage.objects.filter(
            Q(sender=self.request.user) |
            Q(receiver=self.request.user) 
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if instance.receiver == user:
            if not instance.is_read:
                instance.is_read = True
                instance.read_time = now()
            instance.save(update_fields['is_read', 'read_time'])
        serializer = self.get_serializer(instance)
        return Response(
            {
                'message': "Text Message detail successfully",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

text_message_detail_api_view = TextMessageDetailAPIView.as_view()



class TextMessageUpdateAPIView(BaseTextMessageAPIView, generics.UpdateAPIView):

    def get_queryset(self):
        return TextMessage.objects.filter(
            Q(sender=self.request.user) |
            Q(receiver=self.request.user) 
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": "Text Message updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Failed to update Text Message",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

text_message_update_api_view = TextMessageUpdateAPIView.as_view()



class TextMessageDeleteAPIView(BaseTextMessageAPIView, generics.DestroyAPIView):

    def get_queryset(self):
        return TextMessage.objects.filter(
            Q(sender=self.request.user) |
            Q(receiver=self.request.user) 
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "Text Message deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )

text_message_delete_api_view = TextMessageDeleteAPIView.as_view()


class FilterEmployeeCommunicationApiView(APIView):
    pass
