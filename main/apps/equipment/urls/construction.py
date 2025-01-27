from django.urls import path
from ..views import hydro_station



urlpatterns = [
    path(
        'task-create/', 
        hydro_station.construction_task_create_api_view, 
        name='construction_create'
    ),
    path(
        'task-list/', 
        hydro_station.construction_task_list_api_view, 
        name='construction_list'
    ),
    path(
        'task-detail/<int:pk>/', 
        hydro_station.construction_task_detail_api_view, 
        name='construction_retrieve'
    ),
    path(
        'task-update/<int:pk>/', 
        hydro_station.construction_task_update_api_view, 
        name='construction_update'
    ),
    path(
        'task-delete/<int:pk>/', 
        hydro_station.construction_task_delete_api_view, 
        name='construction_delete'
    ),
    path(
        'monthly-expense-create/', 
        hydro_station.monthly_expense_create_api_view, 
        name='construction_create'
    ),
    path(
        'monthly-expense-list/', 
        hydro_station.monthly_expense_list_api_view, 
        name='construction_list'
    ),
    path(
        'monthly-expense-detail/<int:pk>/', 
        hydro_station.monthly_expense_detail_api_view, 
        name='construction_retrieve'
    ),
    path(
        'monthly-expense-update/<int:pk>/', 
        hydro_station.monthly_expense_update_api_view, 
        name='construction_update'
    ),
    path(
        'monthly-expense-delete/<int:pk>/', 
        hydro_station.monthly_expense_delete_api_view, 
        name='construction_delete'
    ),
    
]


