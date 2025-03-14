from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.equipment.models.hydro_station import FinancialResource, HydroStation
from ..serializers import hydro_station as hydro_station_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response



class HydroStationCreateAPIView(generics.CreateAPIView):
    queryset = HydroStation.objects.all()
    serializer_class = hydro_station_serializer.HydroStationSerializer
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

hydro_station_create_api_view = HydroStationCreateAPIView.as_view()



class HydroStationListAPIView(generics.ListAPIView):
    serializer_class = hydro_station_serializer.HydroStationSerializer
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
        queryset = HydroStation.objects.all()
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

hydro_station_list_api_view = HydroStationListAPIView.as_view()




class HydroStationDetailAPIView(generics.RetrieveAPIView):
    queryset = HydroStation.objects.all()
    serializer_class = hydro_station_serializer.HydroStationSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data}, status = status.HTTP_200_OK)

hydro_station_detail_api_view = HydroStationDetailAPIView.as_view()



class HydroStationUpdateAPIView(generics.UpdateAPIView):
    queryset = HydroStation.objects.all()
    serializer_class = hydro_station_serializer.HydroStationSerializer
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
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

hydro_station_update_api_view = HydroStationUpdateAPIView.as_view()
    


class HydroStationDeleteAPIView(generics.DestroyAPIView):
    queryset = HydroStation.objects.all()
    serializer_class = hydro_station_serializer.HydroStationSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Successfully deleted!'},
            status=status.HTTP_204_NO_CONTENT
        )

hydro_station_delete_api_view = HydroStationDeleteAPIView.as_view()



class FinancialResourceCreateAPIView(generics.CreateAPIView):
    queryset = FinancialResource.objects.all()
    serializer_class = hydro_station_serializer.FinancialResourceSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

financial_resource_create_api_view = FinancialResourceCreateAPIView.as_view()



class FinancialResourceListAPIView(generics.ListAPIView):
    serializer_class = hydro_station_serializer.FinancialResourceSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = FinancialResource.objects.select_related("hydro_station")
        hydro_station = self.request.query_params.get('hydro_station')
        if hydro_station:
            queryset = queryset.filter(hydro_station=hydro_station)
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

financial_resource_list_api_view = FinancialResourceListAPIView.as_view()



class FinancialResourceDetailAPIView(generics.RetrieveAPIView):
    queryset = FinancialResource.objects.all()
    serializer_class = hydro_station_serializer.FinancialResourceSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            status = status.HTTP_200_OK,
            data=serializer.data
        )

financial_resource_detail_api_view = FinancialResourceDetailAPIView.as_view()




class FinancialResourceUpdateAPIView(generics.UpdateAPIView):
    queryset = FinancialResource.objects.all()
    serializer_class = hydro_station_serializer.FinancialResourceSerializer
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

financial_resource_update_api_view = FinancialResourceUpdateAPIView.as_view()
    


class FinancialResourceDeleteAPIView(generics.DestroyAPIView):
    queryset = FinancialResource.objects.all()
    serializer_class = hydro_station_serializer.FinancialResourceSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Successfully deleted!'},
            status=status.HTTP_204_NO_CONTENT
        )

financial_resource_delete_api_view = FinancialResourceDeleteAPIView.as_view()