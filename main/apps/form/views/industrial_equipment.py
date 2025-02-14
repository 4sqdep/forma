from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.equipment.models.industrial_equipment import IndustrialAsset, IndustrialEquipment
from ..serializers import industrial_equipment as industrial_equipment_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response



class IndustrialEquipmentCreateAPIView(generics.CreateAPIView):
    queryset = IndustrialEquipment.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialEquipmentCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                'message': 'Successfully created',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
            )
        return Response(
            {
                'message': 'Failed to create',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

industrial_equipment_create_api_view = IndustrialEquipmentCreateAPIView.as_view()


class IndustrialEquipmentListAPIView(generics.ListAPIView):
    serializer_class = industrial_equipment_serializer.IndustrialEquipmentListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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
        hydro_station_id = self.kwargs.get('hydro_station_id')
        query = """
            SELECT ie.*
            FROM equipment_industrialequipment ie
            WHERE (%s IS NULL OR ie.hydro_station_id = %s);
        """
        return IndustrialEquipment.objects.raw(query, [hydro_station_id, hydro_station_id])

    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.get_pagination_class()

        if paginator:
            paginator = paginator()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", None)
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data = Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return response_data

industrial_equipment_list_api_view = IndustrialEquipmentListAPIView.as_view()




class IndustrialEquipmentDetailAPIView(generics.RetrieveAPIView):
    queryset = IndustrialEquipment.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialEquipmentListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            status = status.HTTP_200_OK,
            data=serializer.data
        )

industrial_equipment_detail_api_view = IndustrialEquipmentDetailAPIView.as_view()



class IndustrialEquipmentUpdateAPIView(generics.UpdateAPIView):
    queryset = IndustrialEquipment.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialEquipmentCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=serializer.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Successfully updated'},
                status = status.HTTP_200_OK,
                data=serializer.data
                )
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

industrial_equipment_update_api_view = IndustrialEquipmentUpdateAPIView.as_view()
    


class IndustrialEquipmentDeleteAPIView(generics.DestroyAPIView):
    queryset = IndustrialEquipment.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialEquipmentListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Successfully deleted!'},
            status=status.HTTP_204_NO_CONTENT
        )

industrial_equipment_delete_api_view = IndustrialEquipmentDeleteAPIView.as_view()



class IndustrialAssetCreateAPIView(generics.CreateAPIView):
    queryset = IndustrialAsset.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialAssetCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                'message': 'Successfully created',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
            )
        return Response(
            {
                'message': 'Failed to create',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

industrial_asset_create_api_view = IndustrialAssetCreateAPIView.as_view()



class IndustrialAssetListAPIView(generics.ListAPIView):
    serializer_class = industrial_equipment_serializer.IndustrialAssetListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = IndustrialAsset.objects.select_related("industrial_equipment", "measurement")
        industrial_equipment_id = self.kwargs.get('industrial_equipment_id')
        hydro_station_id = self.kwargs.get('hydro_station_id')
        if industrial_equipment_id and hydro_station_id:
            queryset = queryset.filter(
                industrial_equipment=industrial_equipment_id,
                industrial_equipment__hydro_station=hydro_station_id
                )
        return queryset
    
    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.get_pagination_class()

        if paginator:
            paginator = paginator()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", None)
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data = Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return response_data

industrial_asset_list_api_view = IndustrialAssetListAPIView.as_view()



class IndustrialAssetDetailAPIView(generics.RetrieveAPIView):
    queryset = IndustrialAsset.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialAssetListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            status = status.HTTP_200_OK,
            data=serializer.data
        )

industrial_asset_detail_api_view = IndustrialAssetDetailAPIView.as_view()




class IndustrialAssetUpdateAPIView(generics.UpdateAPIView):
    queryset = IndustrialAsset.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialAssetCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=serializer.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Successfully Updated'},
                status = status.HTTP_200_OK,
                data=serializer.data
                )
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

industrial_asset_update_api_view = IndustrialAssetUpdateAPIView.as_view()
    


class IndustrialAssetDeleteAPIView(generics.DestroyAPIView):
    queryset = IndustrialAsset.objects.all()
    serializer_class = industrial_equipment_serializer.IndustrialAssetListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Successfully deleted!'},
            status=status.HTTP_204_NO_CONTENT
        )

industrial_asset_delete_api_view = IndustrialAssetDeleteAPIView.as_view()