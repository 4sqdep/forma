from django.urls import path
from . import views


urlpatterns = [
    path(
        "create/", 
        views.checklist_create_api_view,
        name='checklist_create'
    ),
    path(
        "list/", 
        views.checklist_list_api_view,
        name='checklist_list'
    ),
    path(
        "detail/<int:pk>/", 
        views.checklist_detail_api_view, 
        name="checklist_detail"
    ),
]


