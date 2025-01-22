from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.reestr.models.construction import ConstructionTask, MonthlyExpense
from main.apps.reestr.utils.calculations import(
    constructions_total_cost, 
    constructions_total_cost_for_month, 
    get_difference, 
    get_fact_sum, 
    get_total_difference, 
    get_total_fact_sum, get_total_year_sum, 
    total_year_calculation_horizontally
)
from ..serializers import construction as construction_task_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from django.db.models import Sum
from decimal import Decimal



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
                # {'message': 'Successfully created'},
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
        queryset = ConstructionTask.objects.all()
        return queryset

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
        queryset = MonthlyExpense.objects.all()
        next_stage_document_id = self.request.query_params.get('next_stage_document')
        if next_stage_document_id:
            queryset = queryset.filter(construction_task__next_stage_document_id=next_stage_document_id)
        return queryset
    
    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        next_stage_document_id = self.request.query_params.get('next_stage_document')
        queryset = self.get_queryset()
        paginator = self.get_pagination_class()

        constructions_total = constructions_total_cost(next_stage_document_id)
        constructions_monthly = constructions_total_cost_for_month(queryset)
        yearly_sums = get_total_year_sum(queryset)
        yearly_horizontal = total_year_calculation_horizontally(queryset)
        fact_sums = get_fact_sum(queryset)
        total_fact_sums = get_total_fact_sum(queryset)
        differences = get_difference(queryset)
        total_differences = get_total_difference(queryset)

        if paginator:
            paginator = paginator()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data.update({
                "constructions_total_cost": constructions_total,
                "constructions_total_cost_for_month": constructions_monthly,
                "total_year_sums": yearly_sums,
                "total_year_calculation_horizontally": yearly_horizontal,
                "fact_sums": fact_sums,
                "total_fact_sums": total_fact_sums,
                "difference_amount": differences,
                "total_difference_amount": total_differences,
                "status_code": status.HTTP_200_OK,
                "data": response_data.data.pop("results", None),
            })
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data = Response(
                {
                    'data': serializer.data,
                    'constructions_total_cost': constructions_total,
                    'constructions_total_cost_for_month': constructions_monthly,
                    'total_year_sums': yearly_sums,
                    'total_year_calculation_horizontally': yearly_horizontal,
                    'fact_sums': fact_sums,
                    'total_fact_sums': total_fact_sums,
                    'difference_amount': differences,
                    'total_difference_amount': total_differences,
                },
                status=status.HTTP_200_OK
            )
        return response_data

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