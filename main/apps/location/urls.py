from django.urls import path
from . import views


urlpatterns = [
    path(
        "country-list/", 
        views.country_list_api_view,
        name='country_list'
    ),
    path(
        "country-detail/<int:pk>/", 
        views.country_retrieve_api_view, 
        name="country_retrieve"
    ),
    path(
        "region-list/", 
        views.region_list_api_view,
        name='region_list'
    ),
    path(
        "region-detail/<int:pk>/", 
        views.region_retrieve_api_view, 
        name="region_retrieve"
    ),
    path(
        "district-list/", 
        views.district_list_api_view,
        name='district_list'
    ),
    path(
        "district-detail/<int:pk>/", 
        views.district_retrieve_api_view, 
        name="district_retrieve"
    ),
]


