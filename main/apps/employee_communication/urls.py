from django.urls import path
from . import views



urlpatterns = [
    # Employee Communication
    path(
        'create/', 
        views.employee_communication_create_api_view, 
        name='employee_communication_create'
    ),
    path(
        'list/', 
        views.employee_communication_list_api_view, 
        name='employee_communication_list'
    ),
    path(
        '<int:pk>/detail/', 
        views.employee_communication_detail_api_view, 
        name='employee_communication_retrieve'
    ),
    path(
        '<int:pk>/update/', 
        views.employee_communication_update_api_view, 
        name='employee_communication_update'
    ),
    path(
        '<int:pk>/delete/', 
        views.employee_communication_delete_api_view, 
        name='employee_communication_delete'
    ), 

    # File Message
    path(
        'file-message/create/', 
        views.file_message_create_api_view, 
        name='file_message_create'
    ),
    path(
        'file-message/<int:employee_communication>/list/', 
        views.file_message_list_api_view, 
        name='file_message_list'
    ),
    path(
        'file-message/<int:pk>/detail/', 
        views.file_message_detail_api_view, 
        name='file_message_retrieve'
    ),
    path(
        'file-message/<int:pk>/update/', 
        views.file_message_update_api_view, 
        name='file_message_update'
    ),
    path(
        'file-message/<int:pk>/delete/', 
        views.file_message_delete_api_view, 
        name='file_message_delete'
    ), 

    # Text Message
    path(
        'text-message/create/', 
        views.text_message_create_api_view, 
        name='text_message_create'
    ),
    path(
        'text-message/<int:employee_communication>/list/', 
        views.text_message_list_api_view, 
        name='text_message_list'
    ),
    path(
        'text-message/<int:pk>/detail/', 
        views.text_message_detail_api_view, 
        name='text_message_retrieve'
    ),
    path(
        'text-message/<int:pk>/update/', 
        views.text_message_update_api_view, 
        name='text_message_update'
    ),
    path(
        'text-message/<int:pk>/delete/', 
        views.text_message_delete_api_view, 
        name='text_message_delete'
    ),   
]


