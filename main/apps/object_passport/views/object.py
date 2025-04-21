from main.apps.common.pagination import CustomPagination
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, status
from rest_framework_simplejwt import authentication
from main.apps.object_passport.filters import ObjectFilter
from main.apps.object_passport.models.object import Object
from main.apps.object_passport.serializers import object as object_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView




class BaseObjectAPIView(generics.GenericAPIView):
    queryset = Object.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ObjectCreateAPIView(BaseObjectAPIView, generics.CreateAPIView):
    serializer_class = object_serializer.ObjectCreateUpdateSerializer

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = ObjectFilter
    serializer_class = object_serializer.ObjectSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("p", openapi.IN_QUERY, description="Pagination parameter", type=openapi.TYPE_STRING),
        ]
    )

    def get_queryset(self):
        queryset = Object.objects.all()
        sub_category = self.kwargs.get('sub_category')

        if sub_category:
            queryset = queryset.filter(object_subcategory=sub_category)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
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
    serializer_class = object_serializer.ObjectSerializer

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
    serializer_class = object_serializer.ObjectCreateUpdateSerializer

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
    serializer_class = object_serializer.ObjectSerializer

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




class AllObjectListAPIView(BaseObjectAPIView, generics.ListAPIView):
    serializer_class = object_serializer.ObjectSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("p", openapi.IN_QUERY, description="Pagination parameter", type=openapi.TYPE_STRING),
        ]
    )

    def get_queryset(self):
        return Object.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
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

all_object_list_api_view = AllObjectListAPIView.as_view()

