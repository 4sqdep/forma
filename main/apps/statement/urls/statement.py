from django.urls import path
from ..views import statement


urlpatterns = [
    path(
        "create/", 
        statement.statement_create_api_view,
        name='statement_create'
    ),
    path(
        "list/", 
        statement.statement_list_api_view,
        name='statement_list'
    ),
    path(
        "detail/<int:pk>/", 
        statement.statement_detail_api_view, 
        name="statement_detail"
    ),
]


