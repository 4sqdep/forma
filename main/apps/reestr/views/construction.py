from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.reestr.models.construction import ConstructionTask, MonthlyExpense
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
        queryset = MonthlyExpense.objects.all()
        return queryset
    
    def get_total_year_sum(self, queryset):
        year_totals = (
            queryset.values(
                'year__id', 
                'year__title',
                'construction_task__id', 
                'construction_task__title'
            ).annotate(total_year_sum=Sum('spent_amount')).order_by('year__title')
        )
        return [
            {
                'year_id': year['year__id'],
                'year_title': year['year__title'],
                'total_year_sum': year['total_year_sum'] or 0,
                'task_title': year['construction_task__title']
            }
            for year in year_totals
        ]
    
    
    def get_fact_sum(self, queryset):
        total_year_sum = self.get_total_year_sum(queryset)
        grouped_data = queryset.values(
            'construction_task__id', 
            'construction_task__title'
        ).annotate(total_spent=Sum('spent_amount')).order_by('construction_task__id')
        each_task_total = [
            {
                'construction_task_id': task['construction_task__id'],
                'construction_task_title': task['construction_task__title'],
                'total_spent': task['total_spent'] or 0
            }
            for task in grouped_data
        ]
        return each_task_total


    # def get_difference(self, queryset):    
    #     grouped_data = queryset.values(
    #         'construction_task__id', 
    #         'construction_task__title', 
    #         'construction_task__total_cost'
    #     )
    #     for task in grouped_data:
    #         fact_sum = self.get_fact_sum(queryset)
    #         for item in fact_sum:
    #             total_spent = item['total_spent']
    #             total_cost = task['construction_task__total_cost'] or 0
    #             difference_amount = total_cost - total_spent
    #             difference_each_task = [
    #                 {
    #                     'task_id': task['construction_task__id'],
    #                     'task_title': task['construction_task__title'],
    #                     'task_difference_amount': difference_amount,
    #                 }
    #             ]
    #     return difference_each_task

    def get_difference(self, queryset):    
        fact_sum = self.get_fact_sum(queryset)

        difference_each_task = []

        processed_task_ids = set()

        grouped_data = queryset.values(
            'construction_task__id', 
            'construction_task__title', 
            'construction_task__total_cost'
        )
        for task in grouped_data:
            if task['construction_task__id'] in processed_task_ids:
                continue
            processed_task_ids.add(task['construction_task__id'])

            task_fact_sum = next((item['total_spent'] for item in fact_sum if item['construction_task_id'] == task['construction_task__id']), 0)
            
            total_cost = task['construction_task__total_cost'] or 0
            difference_amount = total_cost - task_fact_sum
            
            difference_each_task.append({
                'task_id': task['construction_task__id'],
                'task_title': task['construction_task__title'],
                'task_difference_amount': difference_amount,
            })
        return difference_each_task



    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.get_pagination_class()
        total_year_sums = self.get_total_year_sum(queryset)
        fact_sums = self.get_fact_sum(queryset)
        difference_amount = self.get_difference(queryset)

        if paginator:
            paginator = paginator()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["total_year_sums"] = total_year_sums
            response_data.data["fact_sums"] = fact_sums
            response_data.data["difference_amount"] = difference_amount
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", None)
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data = Response(
                {
                    'data': serializer.data,
                    'total_year_sums': total_year_sums,
                    'fact_sums': fact_sums,
                    'difference_amount': difference_amount
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