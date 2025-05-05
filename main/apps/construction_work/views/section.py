from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.construction_work.filters.section import ConstructionInstallationSectionFilter
from main.apps.construction_work.models.section import ConstructionInstallationSection
from main.apps.role.permissions import RolePermissionMixin
from ..serializers import section as section_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Case, When, Value, IntegerField




class ConstructionInstallationSectionAPIView:
    queryset = ConstructionInstallationSection.objects.all()
    serializer_class = section_serializer.ConstructionInstallationSectionSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ConstructionInstallationSectionListCreateAPIView(RolePermissionMixin, ConstructionInstallationSectionAPIView, generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConstructionInstallationSectionFilter
    required_permission = 'can_create'
    object_type = 'construction_installation_section'
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by object title', type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY, description='Filter by start date (YYYY-MM-DD)', type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description='Filter by end date (YYYY-MM-DD)', type=openapi.TYPE_STRING),
            openapi.Parameter('is_forma', openapi.IN_QUERY, description='Filter by is_forma (true/false)', type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('is_file', openapi.IN_QUERY, description='Filter by is_file (true/false)', type=openapi.TYPE_BOOLEAN),
        ]
    )
    def get_queryset(self):
        queryset = ConstructionInstallationSection.objects.all()
        object_id = self.kwargs.get("object")

        if object_id:
            queryset = queryset.filter(object_id=object_id)

        priority_titles = [
            "Bajarilgan ishlar dalolatnoma F-3 F-2",
            "Ijro hujjatlari",
            "Yig'ma jadval",
            "Kerakli ma'lumotlar",
        ]
        queryset = queryset.annotate(
            custom_order=Case(
                *[When(title=title, then=Value(i)) for i, title in enumerate(priority_titles)],
                default=Value(100), 
                output_field=IntegerField()
            )
        ).order_by("custom_order", "id")
        return queryset

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
            'message': "Qurilishni o'rnatish bo'limlari ro'yxati..",
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
            'message': "Qurilishni o'rnatish bo'limlari ro'yxati yaratildi",
            'status_code': status.HTTP_201_CREATED,
            'data': serializer.data,
        }, status=status.HTTP_201_CREATED)

construction_installation_section_list_create_api_view = ConstructionInstallationSectionListCreateAPIView.as_view()



class ConstructionInstallationSectionRetrieveUpdateDeleteAPIView(RolePermissionMixin, ConstructionInstallationSectionAPIView, generics.RetrieveUpdateDestroyAPIView):
    required_permission = None 
    object_type = 'construction_installation_section'

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
        return Response({"message": "ConstructionInstallationSection updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        self.required_permission = 'can_delete'
        instance = self.get_object()
        object_instance = instance.object

        has_permission, message = self.has_permission_for_object(request.user, instance=object_instance)
        if not has_permission:
            return Response({'detail': message}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({"message": "ConstructionInstallationSection deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_section_detail_update_delete_api_view = ConstructionInstallationSectionRetrieveUpdateDeleteAPIView.as_view()