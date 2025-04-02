from main.apps.common.pagination import CustomPagination
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, status
from rest_framework_simplejwt import authentication
from main.apps.object_passport.models.object import Object
from main.apps.object_passport.serializers import object as object_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi





class BaseObjectAPIView(generics.GenericAPIView):
    queryset = Object.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        return getattr(self, 'serializer_class', object_serializer.ObjectCreateUpdateSerializer())


class ObjectCreateAPIView(BaseObjectAPIView, generics.CreateAPIView):
    serializer_class = object_serializer.ObjectCreateUpdateSerializer()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "Object created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to create Object",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

object_create_api_view = ObjectCreateAPIView.as_view() 


class ObjectListAPIView(BaseObjectAPIView, generics.ListAPIView):
    serializer_class = object_serializer.ObjectSerializer()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("p", openapi.IN_QUERY, description="Pagination parameter", type=openapi.TYPE_STRING),
        ]
    )

    def get_queryset(self):
        queryset = Object.objects.all()
        sub_category = self.kwargs.get('sub_category')
        search = self.request.query_params.get('search')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        new = self.request.query_params.get('new')
        old = self.request.query_params.get('old')
        expensive = self.request.query_params.get('expensive')
        cheap = self.request.query_params.get('cheap')
        high_energy = self.request.query_params.get('high_energy')
        low_energy = self.request.query_params.get('low_energy')

        if sub_category:
            queryset = queryset.filter(object_subcategory=sub_category)
        if search:
            queryset = queryset.filter(title__icontains=search)

        if start_date and end_date:
            queryset = queryset.filter(start_date__gte=start_date, end_date__lte=end_date)
        elif start_date:
            queryset = queryset.filter(start_date=start_date)
        elif end_date:
            queryset = queryset.filter(end_date=end_date)

        if new and new.lower() == 'true':
            queryset = queryset.order_by('-created_at')
        elif old and old.lower() == 'true':
            queryset = queryset.order_by('created_at')

        if expensive and expensive.lower() == 'true':
            queryset = queryset.order_by('-total_price')
        elif cheap and cheap.lower() == 'true':
            queryset = queryset.order_by('total_price')

        if high_energy and high_energy.lower() == 'true':
            queryset = queryset.order_by('-object_power')
        elif low_energy and low_energy.lower() == 'true':
            queryset = queryset.order_by('object_power')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        p = self.request.query_params.get('p')

        if p:
            paginator = CustomPagination()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", None)
            return Response({'data': response_data.data}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

object_list_api_view = ObjectListAPIView.as_view()    



class ObjectDetailAPIView(BaseObjectAPIView, generics.RetrieveAPIView):
    serializer_class = object_serializer.ObjectSerializer()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "status_code": status.HTTP_200_OK,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

object_detail_api_view = ObjectDetailAPIView.as_view()



class ObjectUpdateAPIView(BaseObjectAPIView, generics.UpdateAPIView):
    serializer_class = object_serializer.ObjectCreateUpdateSerializer()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": "Object updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Failed to update Object",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

object_update_api_view = ObjectUpdateAPIView.as_view()



class ObjectDeleteAPIView(BaseObjectAPIView, generics.DestroyAPIView):
    serializer_class = object_serializer.ObjectSerializer()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "Object deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )

object_delete_api_view = ObjectDeleteAPIView.as_view()
