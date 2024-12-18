from django.urls import path
from . import views


urlpatterns = [
    path(
        "create/", 
        views.contract_create_api_view,
        name='contract_create'
    ),
    path(
        "list/", 
        views.contract_list_api_view,
        name='contract_list'
    ),
    path(
        "detail/<int:pk>/", 
        views.contract_detail_api_view, 
        name="contract_detail"
    ),
]


