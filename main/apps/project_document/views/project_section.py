from rest_framework.response import Response
from rest_framework import permissions, status
from main.apps.common.pagination import CustomPagination
from rest_framework_simplejwt import authentication
from rest_framework import generics, status, permissions 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from main.apps.project_document.filters.project_section import ProjectSectionFilter
from main.apps.project_document.models.project_section import ProjectSection
from main.apps.project_document.serializers import project_section as project_section_serializer
from django_filters.rest_framework import DjangoFilterBackend
from main.apps.role.permissions import RolePermissionMixin




class BaseProjectSectionAPIView(generics.GenericAPIView):
    queryset = ProjectSection.objects.all()
    serializer_class = project_section_serializer.ProjectSectionSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ProjectSectionCreateAPIView(RolePermissionMixin, BaseProjectSectionAPIView, generics.CreateAPIView):
    required_permission = 'can_create'
    object_type = 'project_document_type'

    def create(self, request, *args, **kwargs):
        has_permission, message = self.has_permission_for_object(request.user)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = project_section_serializer.ProjectSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ProjectSection successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Error creating ProjectSection", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

project_section_create_api_view = ProjectSectionCreateAPIView.as_view()



class ProjectSectionListAPIView(BaseProjectSectionAPIView, generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectSectionFilter

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("document", openapi.IN_QUERY, description="Filter by document ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("name", openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
            openapi.Parameter("file_code", openapi.IN_QUERY, description="Filter by file code", type=openapi.TYPE_STRING),
        ]
    )
    def get_queryset(self):
        project_document_type = self.kwargs.get("project_document_type") 
        queryset = ProjectSection.objects.all()

        if project_document_type:
            queryset = queryset.filter(project_document_type=project_document_type)
        return queryset
    
    def get_pagination_class(self):
        p = self.request.query_params.get('p')
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

        serializer = project_section_serializer.ProjectSectionSerializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

project_section_list_api_view = ProjectSectionListAPIView.as_view()



class ProjectSectionDetailAPIView(BaseProjectSectionAPIView, generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data, "status_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)

project_section_detail_api_view = ProjectSectionDetailAPIView.as_view()



class ProjectSectionUpdateAPIView(RolePermissionMixin, BaseProjectSectionAPIView, generics.UpdateAPIView):
    required_permission = 'can_update'
    object_type = 'project_document_type'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        object_instance = instance.project_document_type.object
        
        has_permission, message = self.has_permission_for_object(request.user, instance=object_instance)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "ProjectSection successfully updated", "status_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({"message": "Error updating ProjectSection", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

project_section_update_api_view = ProjectSectionUpdateAPIView.as_view()



class ProjectSectionDeleteAPIView(RolePermissionMixin, BaseProjectSectionAPIView, generics.DestroyAPIView):
    required_permission = 'can_delete'
    object_type = 'project_document_type'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        object_instance = instance.project_document_type.object
        
        has_permission, message = self.has_permission_for_object(request.user, instance=object_instance)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return Response({"message": "ProjectSection successfully deleted", "status_code": status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)

project_section_delete_api_view = ProjectSectionDeleteAPIView.as_view()

