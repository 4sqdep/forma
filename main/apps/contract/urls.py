from django.urls import path
from main.apps.contract import views


urlpatterns = [
    path(
        'create/',
        views.create_contract_api_view,
        name='create'
    ),
    path(
        '<int:contract_section>/list/',
        views.list_contract_section_api_view,
        name='list'
    ),
    path(
        '<int:pk>/detail/',
        views.detail_contract_section_api_view,
        name='detail'
    ),
    path(
        '<int:pk>/update/',
        views.update_contract_section_api_view,
        name='update'
    ),
    path(
        '<int:pk>/delete/',
        views.delete_contract_section_api_view,
        name='delete'
    ),
##################################
    #File urls
##################################
    path(
        'file/create/',
        views.create_contract_file_api_view,
        name='create'
    ),
    path(
        'file/<int:contract_file>/list/',
        views.list_contract_file_api_view,
        name='list'
    ),
    path(
        'file/<int:pk>/update/',
        views.update_contract_file_api_view,
        name='update'
    ),
    path(
        'file/<int:pk>/delete/',
        views.delete_contract_file_api_view,
        name='delete'
    )
]