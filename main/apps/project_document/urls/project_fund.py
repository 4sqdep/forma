from django.urls import path
from main.apps.project_document.views import project_fund



urlpatterns = [
    path(
        'task/create/', 
        project_fund.construction_task_create_api_view, 
        name='construction_create'
    ),
    path(
        'task/<int:project_document_type>/list/', 
        project_fund.construction_task_list_api_view, 
        name='construction_list'
    ),
    path(
        'task/<int:pk>/detail/', 
        project_fund.construction_task_detail_api_view, 
        name='construction_retrieve'
    ),
    path(
        'task/<int:pk>/update/', 
        project_fund.construction_task_update_api_view, 
        name='construction_update'
    ),
    path(
        'task/<int:pk>/delete/', 
        project_fund.construction_task_delete_api_view, 
        name='construction_delete'
    ),
    path(
        'monthly-expense/create/', 
        project_fund.monthly_expense_create_api_view, 
        name='construction_create'
    ),
    path(
        'monthly-expense/<int:project_document_type>/list/', 
        project_fund.monthly_expense_list_api_view, 
        name='construction_list'
    ),
    path(
        'monthly-expense/<int:pk>/detail/', 
        project_fund.monthly_expense_detail_api_view, 
        name='construction_retrieve'
    ),
    path(
        'monthly-expense/<int:pk>/update/', 
        project_fund.monthly_expense_update_api_view, 
        name='construction_update'
    ),
    path(
        'monthly-expense/<int:pk>/delete/', 
        project_fund.monthly_expense_delete_api_view, 
        name='construction_delete'
    ),
    
]


