from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.construction_work.models.work_volume import MonthlyWorkVolume, WorkCategory, WorkType, WorkVolume
from ..serializers import work_volume as work_volume_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from django.db.models import Sum 





class BaseWorkTypeAPIView:
    queryset = WorkType.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class WorkTypeListCreateAPIView(BaseWorkTypeAPIView, generics.ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return work_volume_serializer.WorkTypeCreateSerializer
        return work_volume_serializer.WorkTypeSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by contractor', type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        object = self.kwargs.get('object')

        if object:
            queryset = queryset.filter(object=object)
        
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data 
        total_plan = sum(item.get('plan') for item in data)
        total_fact = sum(item.get('fact') for item in data)
        total_remained_percent = (total_fact / total_plan) * 100 if total_plan else 0

        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            response.data["total_plan"] = total_plan
            response.data["total_fact"] = total_fact
            response.data["total_remained_percent"] = round(total_remained_percent, 2)
            return response

        return Response({
            'message': "Work Type ro'yxati",
            'status_code': status.HTTP_200_OK,
            "data": serializer.data,
            "total_plan": total_plan,
            "total_fact": total_fact,
            "total_remained_percent": round(total_remained_percent, 2)
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': "Work Type successfully created",
            'status_code': status.HTTP_201_CREATED,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

work_type_list_create_api_view = WorkTypeListCreateAPIView.as_view()



class WorkTypeRetrieveUpdateDeleteAPIView(BaseWorkTypeAPIView, generics.RetrieveUpdateDestroyAPIView):

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return work_volume_serializer.WorkTypeCreateSerializer
        return work_volume_serializer.WorkTypeSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Work Type updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Work Type deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

work_type_detail_update_delete_api_view = WorkTypeRetrieveUpdateDeleteAPIView.as_view()



class BaseWorkCategoryAPIView:
    queryset = WorkCategory.objects.all()
    serializer_class = work_volume_serializer.WorkCategorySerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class WorkCategoryListCreateAPIView(BaseWorkCategoryAPIView, generics.ListCreateAPIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by contractor', type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        object = self.kwargs.get('object')

        if object:
            queryset = queryset.filter(object=object)

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
            'message': "Work Category ro'yxati",
            'status_code': status.HTTP_200_OK,
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': "Work Category successfully created",
            'status_code': status.HTTP_201_CREATED,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

work_category_list_create_api_view = WorkCategoryListCreateAPIView.as_view()



class WorkCategoryRetrieveUpdateDeleteAPIView(BaseWorkCategoryAPIView, generics.RetrieveUpdateDestroyAPIView):

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Work Category updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Work Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

work_category_detail_update_delete_api_view = WorkCategoryRetrieveUpdateDeleteAPIView.as_view()



class BaseWorkVolumeAPIView:
    queryset = WorkVolume.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class WorkVolumeListCreateAPIView(BaseWorkVolumeAPIView, generics.ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return work_volume_serializer.WorkVolumeCreateSerializer
        return work_volume_serializer.WorkVolumeSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by contractor', type=openapi.TYPE_STRING)
        ]
    )
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        work_category = self.kwargs.get('work_category')

        if work_category:
            queryset = queryset.filter(work_category=work_category)
        
        total_plan = queryset.aggregate(Sum('plan'))['plan__sum'] or 0
        total_fact = queryset.aggregate(Sum('fact'))['fact__sum'] or 0
        total_remained_percent = (total_fact / total_plan) * 100 if total_plan else 0

        plan = WorkVolume.objects.all().aggregate(Sum('plan'))['plan__sum']
        completed_volume = WorkVolume.objects.all().aggregate(Sum('fact'))['fact__sum']
        remained_volume = plan - completed_volume
        
        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            response.data['total_plan'] = total_plan
            response.data['total_fact'] = total_fact
            response.data['total_remained_percent'] = round(total_remained_percent, 2)
            response.data['plan'] = plan
            response.data['fact'] = fact
            response.data['remain'] = remain
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': "Work volume ro'yxati",
            'status_code': status.HTTP_200_OK,
            "data": serializer.data,
            "total_plan": total_plan,
            "total_fact": total_fact,
            "total_remained_percent": round(total_remained_percent, 2),
            "completed_volume": completed_volume,
            "remained_volume": remained_volume
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': "Work volume successfully created",
            'status_code': status.HTTP_201_CREATED,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

work_volume_list_create_api_view = WorkVolumeListCreateAPIView.as_view()



class WorkVolumeRetrieveUpdateDeleteAPIView(BaseWorkVolumeAPIView, generics.RetrieveUpdateDestroyAPIView):

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return work_volume_serializer.WorkVolumeCreateSerializer
        return work_volume_serializer.WorkVolumeSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Work volume updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Work volume deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

work_volume_detail_update_delete_api_view = WorkVolumeRetrieveUpdateDeleteAPIView.as_view()



class BaseMonthlyWorkVolumeAPIView:
    queryset = MonthlyWorkVolume.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class MonthlyWorkVolumeListCreateAPIView(BaseMonthlyWorkVolumeAPIView, generics.ListCreateAPIView):
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return work_volume_serializer.MonthlyWorkVolumeCreateSerializer
        return work_volume_serializer.MonthlyWorkVolumeSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by contractor', type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        work_category = self.kwargs.get('work_category')

        if work_category:
            queryset = queryset.filter(work_category=work_category)

        summary_data = queryset.values(
            'work_category_id',
            'work_category__title',
            'work_type_id',
            'work_type__title'
        ).annotate(
            total_plan=(Sum('plan')),
            total_fact=(Sum('fact'))
        )

        for item in summary_data:
            plan = item['total_plan'] or 0
            fact = item['total_fact'] or 0
            item['remained_percent'] = round(((plan - fact) / plan * 100), 2) if plan else 0

        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            response.data['summary'] = summary_data
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': "Monthly Work volume ro'yxati",
            'status_code': status.HTTP_200_OK,
            "data": serializer.data,
            "summary": summary_data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': "Monthly Work volume successfully created",
            'status_code': status.HTTP_201_CREATED,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

monthly_work_volume_list_create_api_view = MonthlyWorkVolumeListCreateAPIView.as_view()



class MonthlyWorkVolumeRetrieveUpdateDeleteAPIView(BaseMonthlyWorkVolumeAPIView, generics.RetrieveUpdateDestroyAPIView):

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return work_volume_serializer.MonthlyWorkVolumeCreateSerializer
        return work_volume_serializer.MonthlyWorkVolumeSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Monthly Work volume updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Monthly Work volume deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

monthly_work_volume_detail_update_delete_api_view = MonthlyWorkVolumeRetrieveUpdateDeleteAPIView.as_view()