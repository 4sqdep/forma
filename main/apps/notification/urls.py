from django.urls import path
from . import views


urlpatterns = [
    path(
        "list/", 
        views.notification_list_api_view,
        name='notification_list'
    ),
    path(
        "detail/<int:pk>/", 
        views.notification_detail_api_view, 
        name="notification_detail"
    ),
]


