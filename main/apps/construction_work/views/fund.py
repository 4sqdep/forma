from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.construction_work.models.fund import ConstructionInstallationProject, MonthlyCompletedTask
from ..serializers import fund as project_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

from ..calculations import(
    constructions_total_cost, 
    get_total_difference, 
    constructions_total_cost_for_month, 
    get_total_year_sum, 
    total_year_calculation_horizontally
)
from decimal import Decimal
from django.db.models.functions import Coalesce
from django.db.models import Sum




class ConstructionInstallationProjectAPIView:
    queryset = ConstructionInstallationProject.objects.all()
    serializer_class = project_serializer.ConstructionInstallationProjectSerializer()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ConstructionInstallationProjectListCreateAPIView(ConstructionInstallationProjectAPIView, generics.ListCreateAPIView):

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



class MonthlyCompletedTaskAPIView:
    queryset = MonthlyCompletedTask.objects.all()
    serializer_class = project_serializer.MonthlyCompletedTaskSerializer()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class MonthlyCompletedTaskListCreateAPIView(MonthlyCompletedTaskAPIView, generics.ListCreateAPIView):
    
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
