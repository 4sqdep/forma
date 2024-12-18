from django.urls import path
from . import views


urlpatterns = [
    path(
        "create/", 
        views.order_create_api_view,
        name='order_create'
    ),
    path(
        "list/", 
        views.order_list_api_view,
        name='order_list'
    ),
    path(
        "detail/<int:pk>/", 
        views.order_detail_api_view, 
        name="order_detail"
    ),
]


