from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.dashboard.models.construction_installation_work import (
    ConstructionInstallationFile, 
    ConstructionInstallationProject, 
    ConstructionInstallationSection, 
    ConstructionInstallationStatistics, 
    MonthlyCompletedTask
)
from ..serializers import construction_installation_work as construction_installation_work_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from django.db.models import Q
from main.apps.dashboard.utils import(
    constructions_total_cost, 
    get_total_difference, 
    constructions_total_cost_for_month, 
    get_total_year_sum, 
    total_year_calculation_horizontally
)
from decimal import Decimal
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.utils.dateparse import parse_date




class ConstructionInstallationSectionAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConstructionInstallationSection.objects.all()


class ConstructionInstallationSectionListCreateAPIView(ConstructionInstallationSectionAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationSectionSerializer

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
        search = self.request.query_params.get("search")
        is_forma = self.request.query_params.get("is_forma")
        is_file = self.request.query_params.get("is_file")
        new = self.request.query_params.get('new')
        old = self.request.query_params.get('old')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if object_id:
            queryset = queryset.filter(object_id=object_id)

        if search:
            queryset = queryset.filter(title__icontains=search)

        if is_forma:
            queryset = queryset.filter(is_forma=is_forma.lower() in ["true", "1"])

        if is_file:
            queryset = queryset.filter(is_file=is_file.lower() in ["true", "1"])

        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(created_at__date__gte=start_date_parsed)

        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(created_at__date__lte=end_date_parsed)

        if new and new.lower() == 'true':
            queryset = queryset.order_by('-created_at')

        if old and old.lower() == 'true':
            queryset = queryset.order_by('created_at')

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED) 

construction_installation_section_list_create_api_view = ConstructionInstallationSectionListCreateAPIView.as_view()



class ConstructionInstallationSectionRetrieveUpdateDeleteAPIView(ConstructionInstallationSectionAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationSectionSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "ConstructionInstallationSection updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "ConstructionInstallationSection deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_section_detail_update_delete_api_view = ConstructionInstallationSectionRetrieveUpdateDeleteAPIView.as_view()



class ConstructionInstallationFileAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConstructionInstallationFile.objects.all().order_by('file_code')


class ConstructionInstallationFileListCreateAPIView(ConstructionInstallationFileAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationFileSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by object title', type=openapi.TYPE_STRING),
        ]
    )

    def get_queryset(self):
        document = self.kwargs.get("document") 
        queryset = ConstructionInstallationFile.objects.all()
        section = self.kwargs.get('section')
        search = self.request.query_params.get('search')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if document:
            queryset = queryset.filter(document=document)
        
        if section:
            queryset = queryset.filter(section=section)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(file_code__icontains=search) 
            )
        
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        elif start_date:
            queryset = queryset.filter(date=start_date)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

construction_installation_file_list_create_api_view = ConstructionInstallationFileListCreateAPIView.as_view()



class ConstructionInstallationFileRetrieveUpdateDeleteAPIView(ConstructionInstallationFileAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationFileSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Construction Installation File updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Construction Installation File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_file_detail_update_delete_api_view = ConstructionInstallationFileRetrieveUpdateDeleteAPIView.as_view()



class ConstructionInstallationStatisticsAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConstructionInstallationStatistics.objects.all()


class ConstructionInstallationStatisticsListCreateAPIView(ConstructionInstallationStatisticsAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationStatisticsSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by contractor', type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        obj = self.kwargs.get('obj')
        # section = request.query_params.get('section')
        # search = request.query_params.get('search')
        # date = request.query_params.get('date')

        # if search:
        #     queryset = queryset.filter(Q(contractor__icontains=search))

        # if section:
        #     queryset = queryset.filter(construction_installation_section=section)

        # if date:
        #     queryset = queryset.filter(date=date)

        if obj:
            queryset = queryset.filter(object_id=obj)

        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

construction_installation_statistics_list_create_api_view = ConstructionInstallationStatisticsListCreateAPIView.as_view()



class ConstructionInstallationStatisticsRetrieveUpdateDeleteAPIView(ConstructionInstallationStatisticsAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationStatisticsSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Construction Installation Statistics updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Construction Installation Statistics deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_statistics_detail_update_delete_api_view = ConstructionInstallationStatisticsRetrieveUpdateDeleteAPIView.as_view()


# ===================== Construction Installation Project Views =====================

class ConstructionInstallationProjectAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConstructionInstallationProject.objects.all()


class ConstructionInstallationProjectListCreateAPIView(ConstructionInstallationProjectAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationProjectSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by project title', type=openapi.TYPE_STRING),
            openapi.Parameter('section', openapi.IN_QUERY, description='Filter by section ID', type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        section = self.kwargs.get('section')

        if section:
            queryset = queryset.filter(section=section)
        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
    
construction_installation_project_list_create_api_view = ConstructionInstallationProjectListCreateAPIView.as_view()



class ConstructionInstallationProjectRetrieveUpdateDeleteAPIView(ConstructionInstallationProjectAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationProjectSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Construction Installation Project updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Construction Installation Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_project_detail_update_delete_api_view = ConstructionInstallationProjectRetrieveUpdateDeleteAPIView.as_view()


# ===================== Monthly Completed Task Views =====================

class MonthlyCompletedTaskAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = MonthlyCompletedTask.objects.all()


class MonthlyCompletedTaskListCreateAPIView(MonthlyCompletedTaskAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.MonthlyCompletedTaskSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
        ]
    )

    def get_queryset(self):
        section = self.kwargs.get('section')
        if not section:
            return MonthlyCompletedTask.objects.none()
        return MonthlyCompletedTask.objects.select_related("construction_installation_project").filter(
            construction_installation_project__section=section
        )

    def list(self, request, *args, **kwargs):
        section = self.kwargs.get('section')
        queryset = self.get_queryset()

        construction_installation_data = {}
        data = []

        total_year_sum = get_total_year_sum(queryset, section)
        for expense in queryset:
            task = expense.construction_installation_project

            if task.id not in construction_installation_data:
                fact_sum = queryset.filter(construction_installation_project__section=section, construction_installation_project=task.id).aggregate(
                    total_spent=Coalesce(Sum("monthly_amount"), Decimal(0))
                )["total_spent"]
                data.append(fact_sum)
                allocated_amount = task.allocated_amount or Decimal(0)
                difference = allocated_amount - fact_sum

                year_sums = total_year_sum.get(task.id, {}).get('year_sums', [])

                construction_installation_data[task.id] = {
                    "construction": {
                        "id": task.id,
                        "title": task.title,
                        "currency": task.currency.title if task.currency else None,
                        "allocated_amount": Decimal(allocated_amount),
                        "fact_sum": Decimal(fact_sum),
                        "difference": Decimal(difference),
                        "year_sums": year_sums,  
                    },
                    "monthly_expense": [],
                }

            construction_installation_data[task.id]["monthly_expense"].append({
                "construction_id": task.id,
                'monthly_exepense_id': expense.id,
                "monthly_amount": Decimal(expense.monthly_amount),
                "date": expense.date.isoformat(),
            })

        allocated_amount = constructions_total_cost(section)
        monthly_totals = constructions_total_cost_for_month(queryset, section)
        year_total_calculations = total_year_calculation_horizontally(queryset, section)
        total_fact_sum = sum(data)
        total_difference = get_total_difference(queryset, section)

        response_data = {
            "construction_installation_data": list(construction_installation_data.values()),
            "allocated_amount": Decimal(allocated_amount),
            "monthly_totals": monthly_totals,
            "total_fact_sum": Decimal(total_fact_sum),
            "year_total_calculations": year_total_calculations,
            "total_difference": Decimal(total_difference),
        }

        return Response(
            {'data': response_data},
            status=status.HTTP_200_OK,
            headers={"message": "Monthly expenses retrieved successfully."}
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(data={"message": "Failed to create Completed Task", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

monthly_completed_task_list_create_api_view = MonthlyCompletedTaskListCreateAPIView.as_view()



class MonthlyCompletedTaskRetrieveUpdateDeleteAPIView(MonthlyCompletedTaskAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.MonthlyCompletedTaskSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Monthly Completed Task updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Monthly Completed Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

monthly_completed_task_detail_update_delete_api_view = MonthlyCompletedTaskRetrieveUpdateDeleteAPIView.as_view()
