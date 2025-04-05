from django.urls import path
from . import views



urlpatterns = [
    path(
        'employee-communication/create/', 
        views.employee_communication_create_api_view, 
        name='employee_communication_create'
    ),
    path(
        'employee-communication/list/', 
        views.employee_communication_list_api_view, 
        name='employee_communication_list'
    ),
    path(
        'employee-communication/<int:pk>/detail/', 
        views.employee_communication_detail_api_view, 
        name='employee_communication_retrieve'
    ),
    path(
        'employee-communication/<int:pk>/update/', 
        views.employee_communication_update_api_view, 
        name='employee_communication_update'
    ),
    path(
        'employee-communication/<int:pk>/delete/', 
        views.employee_communication_delete_api_view, 
        name='employee_communication_delete'
    ),   
]


