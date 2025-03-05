from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.dashboard.models.construction_installation_work import ConstructionFile, Section
from ..serializers import construction_installation_work as construction_installation_work_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q



class SectionAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Section.objects.all()


class SectionListCreateAPIView(SectionAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.SectionSerializer


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by object title', type=openapi.TYPE_STRING),
        ]
    )
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title=search)

        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

section_list_create_api_view = SectionListCreateAPIView.as_view()



class SectionRetrieveUpdateDeleteAPIView(SectionAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.SectionSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Section updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Section deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

section_detail_update_delete_api_view = SectionRetrieveUpdateDeleteAPIView.as_view()



class ConstructionFileAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConstructionFile.objects.all()


class ConstructionFileListCreateAPIView(ConstructionFileAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionFileSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by object title', type=openapi.TYPE_STRING),
            openapi.Parameter('section', openapi.IN_QUERY, description='Filter by section ID', type=openapi.TYPE_INTEGER),
        ]
    )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        section = self.kwargs.get('section')
        search = request.query_params.get('search')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(file_code__icontains=search) | 
                Q(full_name__icontains=search)
            )

        if section:
            queryset = queryset.filter(section=section)

        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

construction_file_list_create_api_view = ConstructionFileListCreateAPIView.as_view()



class ConstructionFileRetrieveUpdateDeleteAPIView(ConstructionFileAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionFileSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Construction File updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Construction File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_file_detail_update_delete_api_view = ConstructionFileRetrieveUpdateDeleteAPIView.as_view()