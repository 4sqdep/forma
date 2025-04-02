from main.apps.project_document.serializers import project_file as document_serializer
from rest_framework.response import Response
from rest_framework import permissions, status
from main.apps.common.pagination import CustomPagination
from rest_framework_simplejwt import authentication
from rest_framework import generics, status, permissions 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from main.apps.project_document.models.project_file import ProjectDocumentFile




class BaseProjectDocumentFileAPIView(generics.GenericAPIView):
    queryset = ProjectDocumentFile.objects.all()
    serializer_class = document_serializer.FileSerializer()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ProjectDocumentFileCreateAPIView(BaseProjectDocumentFileAPIView, generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "File successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Error creating file", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

project_document_file_create_api_view = ProjectDocumentFileCreateAPIView.as_view()



class ProjectDocumentFileListAPIView(BaseProjectDocumentFileAPIView, generics.ListAPIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("document", openapi.IN_QUERY, description="Filter by document ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("name", openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
            openapi.Parameter("file_code", openapi.IN_QUERY, description="Filter by file code", type=openapi.TYPE_STRING),
        ]
    )
    def get_queryset(self):
        document = self.kwargs.get("document") 
        queryset = ProjectDocumentFile.objects.all()
        project_section = self.request.query_params.get("project_section")
        name = self.request.query_params.get("name")
        file_code = self.request.query_params.get("file_code")
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if document:
            queryset = queryset.filter(document=document)
        
        if project_section:
            queryset = queryset.filter(project_section=project_section)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if file_code:
            queryset = queryset.filter(file_code__icontains=file_code)
        
        if start_date and end_date:
            queryset = queryset.filter(calendar__range=[start_date, end_date])

        elif start_date:
            queryset = queryset.filter(calendar=start_date)

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
            return Response(response_data.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

project_document_file_list_api_view = ProjectDocumentFileListAPIView.as_view()



class ProjectDocumentFileDetailAPIView(BaseProjectDocumentFileAPIView, generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data, "status_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)

project_document_file_detail_api_view = ProjectDocumentFileDetailAPIView.as_view()



class ProjectDocumentFileUpdateAPIView(BaseProjectDocumentFileAPIView, generics.UpdateAPIView):

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "File successfully updated", "status_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({"message": "Error updating file", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

project_document_file_update_api_view = ProjectDocumentFileUpdateAPIView.as_view()



class ProjectDocumentFileDeleteAPIView(BaseProjectDocumentFileAPIView, generics.DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "File successfully deleted", "status_code": status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)

project_document_file_delete_api_view = ProjectDocumentFileDeleteAPIView.as_view()