from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.construction_work.models.statistics import ConstructionInstallationStatistics
from main.apps.role.permissions import RolePermissionMixin
from ..serializers import statistics as statistics_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response





class ConstructionInstallationStatisticsAPIView:
    queryset = ConstructionInstallationStatistics.objects.all()
    serializer_class = statistics_serializer.ConstructionInstallationStatisticsSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ConstructionInstallationStatisticsListCreateAPIView(RolePermissionMixin, ConstructionInstallationStatisticsAPIView, generics.ListCreateAPIView):
    required_permission = 'can_create'
    object_type = 'construction_installation_statistics'

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by contractor', type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        obj = self.kwargs.get('obj')

        if obj:
            queryset = queryset.filter(object_id=obj)

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
            'message': "Qurilish o'rnatish statistikasi ro'yxati",
            'status_code': status.HTTP_200_OK,
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        has_permission, message = self.has_permission_for_object(request.user)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': "Qurilish o'rnatish statistikasi ro'yxati yaratildi..",
            'status_code': status.HTTP_201_CREATED,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

construction_installation_statistics_list_create_api_view = ConstructionInstallationStatisticsListCreateAPIView.as_view()



class ConstructionInstallationStatisticsRetrieveUpdateDeleteAPIView(RolePermissionMixin, ConstructionInstallationStatisticsAPIView, generics.RetrieveUpdateDestroyAPIView):
    required_permission = None 
    object_type = 'construction_installation_statistics'

    def update(self, request, *args, **kwargs):
        self.required_permission = 'can_update'
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        object_instance = instance.object

        has_permission, message = self.has_permission_for_object(request.user, instance=object_instance)
        if not has_permission:
            return Response({'detail': message}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Construction Installation Statistics updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        self.required_permission = 'can_delete'
        instance = self.get_object()
        object_instance = instance.object

        has_permission, message = self.has_permission_for_object(request.user, instance=object_instance)
        if not has_permission:
            return Response({'detail': message}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return Response({"message": "Construction Installation Statistics deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_statistics_detail_update_delete_api_view = ConstructionInstallationStatisticsRetrieveUpdateDeleteAPIView.as_view()