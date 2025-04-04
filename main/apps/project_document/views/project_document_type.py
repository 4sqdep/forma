from rest_framework.response import Response
from rest_framework import permissions, status
from main.apps.common.pagination import CustomPagination
from rest_framework_simplejwt import authentication
from rest_framework import generics, status, permissions 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from main.apps.project_document.models.project_document_type import ProjectDocumentType
from main.apps.project_document.serializers import project_document_type as document_type_serializer





class BaseProjectDocumentTypeAPIView(generics.GenericAPIView):
    queryset = ProjectDocumentType.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        serializer_class = getattr(self, 'serializer_class', document_type_serializer.ProjectDocumentTypeSerializer)
        return serializer_class(*args, **kwargs)


class ProjectDocumentTypeCreateAPIView(BaseProjectDocumentTypeAPIView, generics.CreateAPIView):
    serializer_class = document_type_serializer.ProjectDocumentTypeCreateSerializer

    def create(self, request, *args, **kwargs):
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
    serializer_class = document_type_serializer.ProjectDocumentTypeSerializer()

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
        object = self.kwargs.get("object")  
        search = self.request.query_params.get("search")
        is_forma = self.request.query_params.get("is_forma")
        is_section = self.request.query_params.get("is_section")
        is_file = self.request.query_params.get("is_file")
        new = self.request.query_params.get('new')
        old = self.request.query_params.get('old')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if object:
            queryset = queryset.filter(object_id=object)

        if search:
            queryset = queryset.filter(name__icontains=search)
        if is_forma:
            queryset = queryset.filter(is_forma=is_forma.lower() in ["true", "1"])
        if is_section:
            queryset = queryset.filter(is_section=is_section.lower() in ["true", "1"])
        if is_file:
            queryset = queryset.filter(is_file=is_file.lower() in ["true", "1"])
        
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)

        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        if new and new.lower() == 'true':
            queryset = queryset.order_by('-created_at')

        if old and old.lower() == 'true':
            queryset = queryset.order_by('created_at')

        return queryset
    
    def get_pagination_class(self):
        p = self.request.query_params.get("p")
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

project_document_type_list_api_view = ProjectDocumentTypeListAPIView.as_view()



class ProjectDocumentTypeDetailAPIView(BaseProjectDocumentTypeAPIView, generics.RetrieveAPIView):
    serializer_class = document_type_serializer.ProjectDocumentTypeSerializer()


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data, "status_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)

project_document_type_detail_api_view = ProjectDocumentTypeDetailAPIView.as_view()



class ProjectDocumentTypeUpdateAPIView(generics.UpdateAPIView):
    serializer_class = document_type_serializer.ProjectDocumentTypeCreateSerializer()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"data": serializer.data, "message": "Hujjat muvaffaqiyatli yangilandi", "status_code": status.HTTP_200_OK},
                status=status.HTTP_200_OK
            )
        return Response({"message": "Hujjatni yangilashda xatolik yuz berdi", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

project_document_type_update_api_view = ProjectDocumentTypeUpdateAPIView.as_view()



class ProjectDocumentTypeDeleteAPIView(generics.DestroyAPIView):
    serializer_class = document_type_serializer.ProjectDocumentTypeSerializer()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Hujjat muvaffaqiyatli o'chirildi", "status_code": status.HTTP_204_NO_CONTENT},
            status=status.HTTP_204_NO_CONTENT
        )

project_document_type_delete_api_view = ProjectDocumentTypeDeleteAPIView.as_view()