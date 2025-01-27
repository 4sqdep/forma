from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.reestr.models.construction import ConstructionTask, MonthlyExpense
from main.apps.reestr.utils.calculations import(
    constructions_total_cost, 
    get_difference, 
    get_total_difference, 
    constructions_total_cost_for_month, 
    get_fact_sum, 
    get_total_fact_sum, 
    get_total_year_sum, 
    total_year_calculation_horizontally
)
from ..serializers import construction as construction_task_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from decimal import Decimal
from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce



class ConstructionTaskCreateAPIView(generics.CreateAPIView):
    queryset = ConstructionTask.objects.all()
    serializer_class = construction_task_serializer.ConstructionTaskSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Successfully created'},
                data=serializer.data, 
                status=status.HTTP_201_CREATED
                )
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

construction_task_create_api_view = ConstructionTaskCreateAPIView.as_view()



class ConstructionTaskListAPIView(generics.ListAPIView):
    serializer_class = construction_task_serializer.ConstructionTaskSerializer
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
        next_stage_document = self.kwargs.get('next_stage_document')
        if next_stage_document:
            return ConstructionTask.objects.filter(next_stage_document=next_stage_document)
        return ConstructionTask.objects.all()

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

construction_task_list_api_view = ConstructionTaskListAPIView.as_view()




class ConstructionTaskDetailAPIView(generics.RetrieveAPIView):
    queryset = ConstructionTask.objects.all()
    serializer_class = construction_task_serializer.ConstructionTaskSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            status = status.HTTP_200_OK,
            data=serializer.data
        )

construction_task_detail_api_view = ConstructionTaskDetailAPIView.as_view()



class ConstructionTaskUpdateAPIView(generics.UpdateAPIView):
    queryset = ConstructionTask.objects.all()
    serializer_class = construction_task_serializer.ConstructionTaskSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=serializer.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Successfully updated'},
                status = status.HTTP_200_OK,
                data=serializer.data
                )
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

construction_task_update_api_view = ConstructionTaskUpdateAPIView.as_view()
    


class ConstructionTaskDeleteAPIView(generics.DestroyAPIView):
    queryset = ConstructionTask.objects.all()
    serializer_class = construction_task_serializer.ConstructionTaskSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Successfully deleted!'},
            status=status.HTTP_204_NO_CONTENT
        )

construction_task_delete_api_view = ConstructionTaskDeleteAPIView.as_view()



class MonthlyExpenseCreateAPIView(generics.CreateAPIView):
    queryset = MonthlyExpense.objects.all()
    serializer_class = construction_task_serializer.MonthlyExpenseCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

monthly_expense_create_api_view = MonthlyExpenseCreateAPIView.as_view()



class MonthlyExpenseListAPIView(generics.ListAPIView):
    serializer_class = construction_task_serializer.MonthlyExpenseListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        next_stage_document = self.kwargs.get('next_stage_document')
        if not next_stage_document:
            return MonthlyExpense.objects.none()
        return MonthlyExpense.objects.select_related("construction_task").filter(
            construction_task__next_stage_document=next_stage_document
        )


    def list(self, request, *args, **kwargs):
        next_stage_document = self.kwargs.get('next_stage_document')
        queryset = self.get_queryset()

        constructions_data = {}
        data = []

        total_year_sum = get_total_year_sum(queryset, next_stage_document)

        for expense in queryset:
            task = expense.construction_task
            if task.id not in constructions_data:
                fact_sum = queryset.filter(construction_task__next_stage_document=next_stage_document, construction_task_id=task.id).aggregate(
                    total_spent=Coalesce(Sum("spent_amount"), Decimal(0))
                )["total_spent"]
                data.append(fact_sum)
                total_cost = task.total_cost or Decimal(0)
                difference = total_cost - fact_sum

                year_sums = total_year_sum.get(task.id, {}).get('year_sums', [])

                constructions_data[task.id] = {
                    "construction": {
                        "id": task.id,
                        "title": task.title,
                        "currency": task.currency.title if task.currency else None,
                        "total_cost": Decimal(total_cost),
                        "fact_sum": Decimal(fact_sum),
                        "difference": Decimal(difference),
                        "year_sums": year_sums,  
                    },
                    "monthly_expense": [],
                }

            constructions_data[task.id]["monthly_expense"].append({
                "construction_id": task.id,
                "spent_amount": Decimal(expense.spent_amount),
                "date": expense.date.isoformat(),
            })

        total_cost = constructions_total_cost(next_stage_document)
        monthly_totals = constructions_total_cost_for_month(queryset, next_stage_document)
        year_total_calculations = total_year_calculation_horizontally(queryset, next_stage_document)
        total_fact_sum = sum(data)
        total_difference = get_total_difference(queryset, next_stage_document)

        response_data = {
            "construction_data": list(constructions_data.values()),
            "total_cost": Decimal(total_cost),
            "monthly_totals": monthly_totals,
            "total_fact_sum": Decimal(total_fact_sum),
            "year_total_calculations": year_total_calculations,
            "total_difference": Decimal(total_difference),
        }

        return Response(response_data, status=status.HTTP_200_OK)

monthly_expense_list_api_view = MonthlyExpenseListAPIView.as_view()



class MonthlyExpenseDetailAPIView(generics.RetrieveAPIView):
    queryset = MonthlyExpense.objects.all()
    serializer_class = construction_task_serializer.MonthlyExpenseListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            status = status.HTTP_200_OK,
            data=serializer.data
        )

monthly_expense_detail_api_view = MonthlyExpenseDetailAPIView.as_view()




class MonthlyExpenseUpdateAPIView(generics.UpdateAPIView):
    queryset = MonthlyExpense.objects.all()
    serializer_class = construction_task_serializer.MonthlyExpenseListSerializer
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

monthly_expense_update_api_view = MonthlyExpenseUpdateAPIView.as_view()
    


class MonthlyExpenseDeleteAPIView(generics.DestroyAPIView):
    queryset = MonthlyExpense.objects.all()
    serializer_class = construction_task_serializer.MonthlyExpenseListSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Successfully deleted!'},
            status=status.HTTP_204_NO_CONTENT
        )

monthly_expense_delete_api_view = MonthlyExpenseDeleteAPIView.as_view()