from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.construction_work.models.statistics import ConstructionInstallationStatistics
from ..serializers import statistics as statistics_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response





class ConstructionInstallationStatisticsAPIView:
    queryset = ConstructionInstallationStatistics.objects.all()
    serializer_class = statistics_serializer.ConstructionInstallationStatisticsSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ConstructionInstallationStatisticsListCreateAPIView(ConstructionInstallationStatisticsAPIView, generics.ListCreateAPIView):

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
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

construction_installation_statistics_list_create_api_view = ConstructionInstallationStatisticsListCreateAPIView.as_view()



class ConstructionInstallationStatisticsRetrieveUpdateDeleteAPIView(ConstructionInstallationStatisticsAPIView, generics.RetrieveUpdateDestroyAPIView):

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Construction Installation Statistics updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Construction Installation Statistics deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_statistics_detail_update_delete_api_view = ConstructionInstallationStatisticsRetrieveUpdateDeleteAPIView.as_view()