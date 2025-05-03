from rest_framework.response import Response
from rest_framework import permissions, status
from main.apps.common.pagination import CustomPagination
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from main.apps.role.models import Role
from main.apps.role.serializers import RoleSerializer




class RoleListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoleSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("object", openapi.IN_QUERY, description="Filter by object ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("title", openapi.IN_QUERY, description="Filter by title", type=openapi.TYPE_STRING),
        ]
    )
    def get_queryset(self):
        queryset = Role.objects.all()
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
            response_data.data['status_code'] = status.HTTP_200_OK
            response_data.data['data'] = response_data.data.pop("results", [])
            return Response({'data': response_data.data, 'status_code': status.HTTP_200_OK},
                            status=status.HTTP_200_OK)
        serializer = RoleSerializer(queryset, many=True)
        return Response({
            'message': 'Role List successfully',
            'status_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

role_list_api_view = RoleListAPIView.as_view()



class RoleRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Role.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': "Role fetched successfully",
            "status_code": status.HTTP_200_OK,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

role_detail_api_view = RoleRetrieveAPIView.as_view()



class RoleUpdateAPIView(generics.UpdateAPIView):
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Role.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': "Role muvaffaqiyatli yangilandi",
                'status_code': status.HTTP_204_NO_CONTENT,
                'data': serializer.data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "message": "Role yangilashda xatolik yuzberdi....",
            'status_code': status.HTTP_400_BAD_REQUEST,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

role_update_api_view = RoleUpdateAPIView.as_view()



class RoleDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Role.objects.all()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Role successfully deleted",
                         "status_code": status.HTTP_204_NO_CONTENT
                         }, status=status.HTTP_204_NO_CONTENT)

role_delete_api_view = RoleDelete.as_view()

