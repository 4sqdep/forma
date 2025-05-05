from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.project_document.calculations import(
    constructions_total_cost, 
    get_total_difference, 
    constructions_total_cost_for_month, 
    get_total_year_sum, 
    total_year_calculation_horizontally
)
from main.apps.project_document.models.project_fund import ConstructionTask, MonthlyExpense
from main.apps.project_document.serializers import project_fund as construction_task_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from decimal import Decimal
from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce
from rest_framework.response import Response

from main.apps.role.permissions import RolePermissionMixin





class BaseConstructionTaskAPIView(generics.GenericAPIView):
    queryset = ConstructionTask.objects.all()
    serializer_class = construction_task_serializer.ConstructionTaskSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ConstructionTaskCreateAPIView(RolePermissionMixin, BaseConstructionTaskAPIView, generics.CreateAPIView):
    required_permission = 'can_create'
    object_type = 'project_document_type'

    def create(self, request, *args, **kwargs):
        has_permission, message = self.has_permission_for_object(request.user)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(data={"message": "Failed to create Construction Task", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

construction_task_create_api_view = ConstructionTaskCreateAPIView.as_view()



class ConstructionTaskListAPIView(BaseConstructionTaskAPIView, generics.ListAPIView):

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
        project_document_type = self.kwargs.get('project_document_type')
        if project_document_type:
            return ConstructionTask.objects.filter(project_document_type=project_document_type)
        return ConstructionTask.objects.all()

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
        return Response(data={"status_code": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK)

construction_task_list_api_view = ConstructionTaskListAPIView.as_view()



class ConstructionTaskDetailAPIView(BaseConstructionTaskAPIView, generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
construction_task_detail_api_view = ConstructionTaskDetailAPIView.as_view()



class ConstructionTaskUpdateAPIView(RolePermissionMixin, BaseConstructionTaskAPIView, generics.UpdateAPIView):
    required_permission = 'can_update'
    object_type = 'project_document_type'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        object_instance = instance.project_document_type.object
        
        has_permission, message = self.has_permission_for_object(request.user, instance=object_instance)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(data={"message": "Failed to update Construction Task", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

construction_task_update_api_view = ConstructionTaskUpdateAPIView.as_view()



class ConstructionTaskDeleteAPIView(RolePermissionMixin, BaseConstructionTaskAPIView, generics.DestroyAPIView):
    required_permission = 'can_delete'
    object_type = 'project_document_type'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        object_instance = instance.project_document_type.object
        
        has_permission, message = self.has_permission_for_object(request.user, instance=object_instance)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return Response(data={"message": "Construction Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_task_delete_api_view = ConstructionTaskDeleteAPIView.as_view()



class BaseMonthlyExpenseAPIView(generics.GenericAPIView):
    queryset = MonthlyExpense.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = getattr(self, 'serializer_class', construction_task_serializer.MonthlyExpenseListSerializer)
        return serializer_class(*args, **kwargs)



class MonthlyExpenseCreateAPIView(RolePermissionMixin, BaseMonthlyExpenseAPIView, generics.CreateAPIView):
    serializer_class = construction_task_serializer.MonthlyExpenseCreateSerializer
    required_permission = 'can_create'
    object_type = 'project_document_type'

    def create(self, request, *args, **kwargs):
        has_permission, message = self.has_permission_for_object(request.user)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(data={"message": "Failed to create Monthly Expense", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

monthly_expense_create_api_view = MonthlyExpenseCreateAPIView.as_view()



class MonthlyExpenseListAPIView(BaseMonthlyExpenseAPIView, generics.ListAPIView):
    serializer_class = construction_task_serializer.MonthlyExpenseListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING
            ),
        ]
    )

    def get_queryset(self):
        project_document_type = self.kwargs.get('project_document_type')
        if not project_document_type:
            return MonthlyExpense.objects.none()
        return MonthlyExpense.objects.select_related("construction_task").filter(
            construction_task__project_document_type=project_document_type
        )

    def list(self, request, *args, **kwargs):
        project_document_type = self.kwargs.get('project_document_type')
        queryset = self.get_queryset()

        constructions_data = {}
        data = []

        total_year_sum = get_total_year_sum(queryset, project_document_type)

        for expense in queryset:
            task = expense.construction_task
            if task.id not in constructions_data:
                fact_sum = queryset.filter(construction_task__project_document_type=project_document_type, construction_task_id=task.id).aggregate(
                    total_spent=Coalesce(Sum("spent_amount"), Decimal(0))
                )["total_spent"]
                data.append(fact_sum)
                total = task.total_cost or Decimal(0)
                difference = total - fact_sum

                year_sums = total_year_sum.get(task.id, {}).get('year_sums', [])

                constructions_data[task.id] = {
                    "construction": {
                        "id": task.id,
                        "title": task.title,
                        "currency": task.currency.title if task.currency else None,
                        "total_cost": Decimal(total),
                        "fact_sum": Decimal(fact_sum),
                        "difference": Decimal(difference),
                        "year_sums": year_sums,  
                    },
                    "monthly_expense": [],
                }

            constructions_data[task.id]["monthly_expense"].append({
                "construction_id": task.id,
                'monthly_exepense_id': expense.id,
                "spent_amount": Decimal(expense.spent_amount),
                "date": expense.date.isoformat(),
            })

        total_cost = constructions_total_cost(project_document_type)
        monthly_totals = constructions_total_cost_for_month(queryset, project_document_type)
        year_total_calculations = total_year_calculation_horizontally(queryset, project_document_type)
        total_fact_sum = sum(data)
        total_difference = get_total_difference(queryset, project_document_type)

        response_data = {
            "construction_data": list(constructions_data.values()),
            "total_cost": Decimal(total_cost),
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

monthly_expense_list_api_view = MonthlyExpenseListAPIView.as_view()



class MonthlyExpenseDetailAPIView(BaseMonthlyExpenseAPIView, generics.RetrieveAPIView):
    serializer_class = construction_task_serializer.MonthlyExpenseListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

monthly_expense_detail_api_view = MonthlyExpenseDetailAPIView.as_view()



class MonthlyExpenseUpdateAPIView(RolePermissionMixin, BaseMonthlyExpenseAPIView, generics.UpdateAPIView):
    serializer_class = construction_task_serializer.MonthlyExpenseListSerializer
    required_permission = 'can_update'
    object_type = 'project_document_type'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        object_instance = instance.construction_task.project_document_type.object
        
        has_permission, message = self.has_permission_for_object(request.user, instance=object_instance)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(data={"message": "Failed to update Monthly Expense", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

monthly_expense_update_api_view = MonthlyExpenseUpdateAPIView.as_view()



class MonthlyExpenseDeleteAPIView(RolePermissionMixin, BaseMonthlyExpenseAPIView, generics.DestroyAPIView):
    serializer_class = construction_task_serializer.MonthlyExpenseListSerializer
    required_permission = 'can_delete'
    object_type = 'project_document_type'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        object_instance = instance.construction_task.project_document_type.object
        
        has_permission, message = self.has_permission_for_object(request.user, instance=object_instance)
        if not has_permission:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return Response(data={"message": "Monthly Expense deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

monthly_expense_delete_api_view = MonthlyExpenseDeleteAPIView.as_view()