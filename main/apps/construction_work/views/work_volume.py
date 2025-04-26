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

    def _calculate_totals(self, object):
        queryset = self.get_queryset().filter(object=object)
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        category_totals = WorkCategory.objects.filter(object=object).aggregate(
            total_plan_amount=Sum('plan_amount') or 0,
            total_fact_amount=Sum('fact_amount') or 0
        )

        total_plan_amount = category_totals['total_plan_amount'] or 0
        total_fact_amount = category_totals['total_fact_amount'] or 0
        total_remained_amount = total_plan_amount - total_fact_amount
        total_completed_amount_percent = (total_fact_amount / total_plan_amount * 100) if total_plan_amount else 0
        currency = queryset.first().object.currency.title if queryset.exists() else ""

        return {
            "total_plan_amount": total_plan_amount,
            "total_fact_amount": total_fact_amount,
            "total_remained_amount": total_remained_amount,
            "total_completed_amount_percent": int(round(total_completed_amount_percent, 2)),
            "currency": currency,
            "data": data
        }


    def get(self, request, *args, **kwargs):
        object = self.kwargs.get('object')
        totals = self._calculate_totals(object)

        queryset = self.get_queryset()
        paginator = CustomPagination() if request.query_params.get('p') else None

        if paginator:
            page = paginator.paginate_queryset(queryset.filter(object=object), request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data.update({
                "status_code": status.HTTP_200_OK,
                "data": response.data.pop("results", []),
                "total_plan_amount": totals["total_plan_amount"],
                "total_fact_amount": totals["total_fact_amount"],
                "total_remained_amount": totals["total_remained_amount"],
                "total_completed_amount_percent": totals["total_completed_amount_percent"],
                "currency": totals["currency"]
            })
            return response

        return Response({
            "message": "Work Type ro'yxati",
            "status_code": status.HTTP_200_OK,
            "data": totals["data"],
            "total_plan_amount": totals["total_plan_amount"],
            "total_fact_amount": totals["total_fact_amount"],
            "total_remained_amount": totals["total_remained_amount"],
            "total_completed_amount_percent": totals["total_completed_amount_percent"],
            "currency": totals["currency"]
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
        total_completed_percent = total_fact / total_plan * 100 if total_plan else 0
        total_remained_volume = total_plan - total_fact

        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            response.data['total_plan'] = total_plan
            response.data['total_fact'] = total_fact
            response.data['total_completed_percent'] = int(round(total_completed_percent, 2))
            response.data['total_remained_volume'] = total_remained_volume
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': "Work volume ro'yxati",
            'status_code': status.HTTP_200_OK,
            "data": serializer.data,
            "total_plan": total_plan,
            "total_fact": total_fact,
            "total_completed_percent": int(round(total_completed_percent, 2)),
            "total_remained_volume": total_remained_volume
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
        work_volume = self.request.query_params.get('work_volume')

        if work_category:
            queryset = queryset.filter(work_volume__work_category=work_category, work_volume=work_volume)

        summary_data = queryset.values(
            'work_volume__work_category_id',
            'work_volume__work_category__title',
            'work_volume__work_type_id',
            'work_volume__work_type__title'
        ).annotate(
            total_plan=(Sum('plan')),
            total_fact=(Sum('fact'))
        )

        for item in summary_data:
            plan = item['total_plan'] or 0
            fact = item['total_fact'] or 0
            item['completed_percent'] = int(round((fact / plan * 100), 2)) if plan else 0

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