from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.reestr.models.currency import Currency
from ..serializers import currency as currency_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response




class CurrencyCreateAPIView(generics.CreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = currency_serializer.CurrencySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

currency_create_api_view = CurrencyCreateAPIView.as_view()



class CurrencyListAPIView(generics.ListAPIView):
    serializer_class = currency_serializer.CurrencySerializer
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
        queryset = Currency.objects.all()
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

currency_list_api_view = CurrencyListAPIView.as_view()



class CurrencyDetailAPIView(generics.RetrieveAPIView):
    queryset = Currency.objects.all()
    serializer_class = currency_serializer.CurrencySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            status = status.HTTP_200_OK,
            data=serializer.data
        )

currency_detail_api_view = CurrencyDetailAPIView.as_view()



class CurrencyUpdateAPIView(generics.UpdateAPIView):
    queryset = Currency.objects.all()
    serializer_class = currency_serializer.CurrencySerializer
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

currency_update_api_view = CurrencyUpdateAPIView.as_view()
    


class CurrencyDeleteAPIView(generics.DestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = currency_serializer.CurrencySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Successfully deleted!'},
            status=status.HTTP_204_NO_CONTENT
        )

currency_delete_api_view = CurrencyDeleteAPIView.as_view()