from django.urls import path
from ..views import measurement


urlpatterns = [
    path(
        "create/", 
        measurement.measurement_create_api_view,
        name='measurement_create'
    ),
    path(
        "list/", 
        measurement.measurement_list_api_view,
        name='measurement_list'
    ),
    path(
        "detail/<int:pk>/", 
        measurement.measurement_detail_api_view, 
        name="measurement_detail"
    ),
]


