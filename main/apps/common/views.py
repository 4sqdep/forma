from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.models import Currency, Measurement
from main.apps.common.pagination import CustomPagination
from . import serializers as common_serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache


CACHE_TIMEOUT = 60 * 5 



class CurrencyCreateAPIView(generics.CreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = common_serializers.CurrencySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("currency_list")  
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"message": "Failed to create Currency", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

currency_create_api_view = CurrencyCreateAPIView.as_view()


class CurrencyListAPIView(generics.ListAPIView):
    serializer_class = common_serializers.CurrencySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
        cache_key = "currency_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        queryset = Currency.objects.all()
        cache.set(cache_key, queryset, CACHE_TIMEOUT) 
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
            return response_data

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)

currency_list_api_view = CurrencyListAPIView.as_view()



class CurrencyDetailAPIView(generics.RetrieveAPIView):
    queryset = Currency.objects.all()
    serializer_class = common_serializers.CurrencySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

currency_detail_api_view = CurrencyDetailAPIView.as_view()



class CurrencyUpdateAPIView(generics.UpdateAPIView):
    queryset = Currency.objects.all()
    serializer_class = common_serializers.CurrencySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            cache.delete("currency_list")  
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={"message": "Failed to update Currency", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

currency_update_api_view = CurrencyUpdateAPIView.as_view()



class CurrencyDeleteAPIView(generics.DestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = common_serializers.CurrencySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        cache.delete("currency_list")  
        return Response(data={"message": "Currency deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

currency_delete_api_view = CurrencyDeleteAPIView.as_view()



class MeasurementCreateAPIView(generics.CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = common_serializers.MeasurementSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"message": "Failed to create Measurement", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

measurement_create_api_view = MeasurementCreateAPIView.as_view()



class MeasurementListAPIView(generics.ListAPIView):
    serializer_class = common_serializers.MeasurementSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
        cache_key = "measurement_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        queryset = Measurement.objects.all()
        cache.set(cache_key, queryset, CACHE_TIMEOUT) 
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
            return response_data

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)

measurement_list_api_view = MeasurementListAPIView.as_view()



class MeasurementDetailAPIView(generics.RetrieveAPIView):
    queryset = Measurement.objects.all()
    serializer_class = common_serializers.MeasurementSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

measurement_detail_api_view = MeasurementDetailAPIView.as_view()



class MeasurementUpdateAPIView(generics.UpdateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = common_serializers.MeasurementSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={"message": "Failed to update Measurement", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

measurement_update_api_view = MeasurementUpdateAPIView.as_view()



class MeasurementDeleteAPIView(generics.DestroyAPIView):
    queryset = Measurement.objects.all()
    serializer_class = common_serializers.MeasurementSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={"message": "Measurement deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

measurement_delete_api_view = MeasurementDeleteAPIView.as_view()
