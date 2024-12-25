from django.urls import path
from ..views import statement_information


urlpatterns = [
    path(
        "create/", 
        statement_information.statement_information_create_api_view,
        name='statement_information_create'
    ),
    path(
        "list/<int:pk>/", 
        statement_information.statement_information_list_api_view,
        name='statement_information_list'
    ),
    path(
        "detail/<int:pk>/", 
        statement_information.statement_information_detail_api_view, 
        name="statement_information_detail"
    ),
]


