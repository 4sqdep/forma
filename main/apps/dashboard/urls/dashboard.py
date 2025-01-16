from django.urls import path
from ..views import dashboard



urlpatterns = [
    path('btn/', dashboard.dashboard_button_api_view, name='btn'),
    path('category-btn/<int:pk>/', dashboard.dashboard_category_button_api_view, name='category-btn'),
    path('sub-btn/<int:pk>/', dashboard.dashboard_subcategory_button_api_view, name='sub-btn'),
    path('sub-btn-post/', dashboard.dashboard_category_button_api_view, name='sub-btn-post'),
]


