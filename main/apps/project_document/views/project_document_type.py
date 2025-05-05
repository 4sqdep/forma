from rest_framework.response import Response
from rest_framework import permissions, status
from main.apps.common.pagination import CustomPagination
from rest_framework_simplejwt import authentication
from rest_framework import generics, status, permissions 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from main.apps.project_document.filters.project_document_type import ProjectDocumentTypeFilter
from main.apps.project_document.models.project_document_type import ProjectDocumentType
from main.apps.project_document.serializers import project_document_type as document_type_serializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Case, When, Value, IntegerField

from main.apps.role.permissions import RolePermissionMixin





class BaseProjectDocumentTypeAPIView(generics.GenericAPIView):
    queryset = ProjectDocumentType.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        serializer_class = getattr(self, 'serializer_class', document_type_serializer.ProjectDocumentTypeSerializer)
        return serializer_class(*args, **kwargs)


class ProjectDocumentTypeCreateAPIView(RolePermissionMixin, BaseProjectDocumentTypeAPIView, generics.CreateAPIView):
    serializer_class = document_type_serializer.ProjectDocumentTypeCreateSerializer
    required_permission = 'can_create'
    object_type = 'project_document_type'

    def create(self, request, *args, **kwargs):
        has_permission, message = self.has_permission_for_object(request.user)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(
                {"message": "Kerakli hujjatlar yaratildi", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Hujjat yaratishda xatolik yuz berdi", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

project_document_type_create_api_view = ProjectDocumentTypeCreateAPIView.as_view()



class ProjectDocumentTypeListAPIView(BaseProjectDocumentTypeAPIView, generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectDocumentTypeFilter
    serializer_class = document_type_serializer.ProjectDocumentTypeSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("p", openapi.IN_QUERY, description="Pagination parameter", type=openapi.TYPE_STRING),
            openapi.Parameter("is_forma", openapi.IN_QUERY, description="Filter by is_forma", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter("is_section", openapi.IN_QUERY, description="Filter by is_section", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter("is_file", openapi.IN_QUERY, description="Filter by is_file", type=openapi.TYPE_BOOLEAN),
        ]
    )

    def get_queryset(self):
        queryset = ProjectDocumentType.objects.all()
        object_id = self.kwargs.get("object")

        if object:
            queryset = queryset.filter(object_id=object_id)
        priority_names = [
            "Birlamchi hujjatlar",
            "Loyiha-smeta hujjatlari",
            "Yig'ma jadval",
            "Kerakli ma'lumotlar",
        ]
        queryset = queryset.annotate(
            custom_order=Case(
                *[When(name=name, then=Value(i)) for i, name in enumerate(priority_names)],
                default=Value(100),  
                output_field=IntegerField()
            )
        ).order_by("custom_order", "id")
        return queryset
    
    def get_pagination_class(self):
        p = self.request.query_params.get("p")
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator_class = self.get_pagination_class()

        if paginator_class:
            paginator = paginator_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", [])
            return Response(response_data.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

project_document_type_list_api_view = ProjectDocumentTypeListAPIView.as_view()



class ProjectDocumentTypeDetailAPIView(BaseProjectDocumentTypeAPIView, generics.RetrieveAPIView):
    serializer_class = document_type_serializer.ProjectDocumentTypeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data, "status_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)

project_document_type_detail_api_view = ProjectDocumentTypeDetailAPIView.as_view()



class ProjectDocumentTypeUpdateAPIView(RolePermissionMixin, BaseProjectDocumentTypeAPIView, generics.UpdateAPIView):
    serializer_class = document_type_serializer.ProjectDocumentTypeCreateSerializer
    required_permission = 'can_update'
    object_type = 'project_document_type'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        object_instance = instance.object
        
        has_permission, message = self.has_permission_for_object(request.user, instance=object_instance)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"data": serializer.data, "message": "Hujjat muvaffaqiyatli yangilandi", "status_code": status.HTTP_200_OK},
                status=status.HTTP_200_OK
            )
        return Response({"message": "Hujjatni yangilashda xatolik yuz berdi", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

project_document_type_update_api_view = ProjectDocumentTypeUpdateAPIView.as_view()



class ProjectDocumentTypeDeleteAPIView(RolePermissionMixin, BaseProjectDocumentTypeAPIView, generics.DestroyAPIView):
    serializer_class = document_type_serializer.ProjectDocumentTypeSerializer
    required_permission = 'can_delete'
    object_type = 'project_document_type'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        object_instance = instance.object
        
        has_permission, message = self.has_permission_for_object(request.user, instance=object_instance)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return Response(
            {"message": "Hujjat muvaffaqiyatli o'chirildi", "status_code": status.HTTP_204_NO_CONTENT},
            status=status.HTTP_204_NO_CONTENT
        )

project_document_type_delete_api_view = ProjectDocumentTypeDeleteAPIView.as_view()