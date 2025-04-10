from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.construction_work.filters.file import ConstructionInstallationFileFilter
from main.apps.construction_work.models.file import ConstructionInstallationFile
from ..serializers import file as file_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend




class ConstructionInstallationFileAPIView:
    queryset = ConstructionInstallationFile.objects.all().order_by('file_code')
    serializer_class = file_serializer.ConstructionInstallationFileSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ConstructionInstallationFileListCreateAPIView(ConstructionInstallationFileAPIView, generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConstructionInstallationFileFilter

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by object title', type=openapi.TYPE_STRING),
        ]
    )

    def get_queryset(self):
        queryset = ConstructionInstallationFile.objects.all()
        section = self.kwargs.get('section')
    
        if section:
            queryset = queryset.filter(section=section)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': "Qurilish o'rnatish fayllar ro'yxati...",
            'status_code': status.HTTP_200_OK,
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': "Qurilish o'rnatish fayllar ro'yxati yaratildi..",
            'status_code': status.HTTP_201_CREATED,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

construction_installation_file_list_create_api_view = ConstructionInstallationFileListCreateAPIView.as_view()



class ConstructionInstallationFileRetrieveUpdateDeleteAPIView(ConstructionInstallationFileAPIView, generics.RetrieveUpdateDestroyAPIView):

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Construction Installation File updated successfully",
            'status_code': status.HTTP_200_OK,
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Construction Installation File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_file_detail_update_delete_api_view = ConstructionInstallationFileRetrieveUpdateDeleteAPIView.as_view()