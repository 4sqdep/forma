from django.urls import path
from .views import DashboardButtonAPIView, DashboardCategoryButtonAPIView, DashboardSubCategoryButtonAPIView
from .testviews import DashboardButtonListView

app_name = "dashboard"

urlpatterns = [
    path('btn/', DashboardButtonAPIView.as_view(), name='btn'),
    path('category-btn/<int:pk>/', DashboardCategoryButtonAPIView.as_view(), name='category-btn'),
    path('sub-btn/<int:pk>/', DashboardSubCategoryButtonAPIView.as_view(), name='sub-btn'),
    path('sub-btn-post/', DashboardCategoryButtonAPIView.as_view(), name='sub-btn-post'),

    path('btn-all/', DashboardButtonListView.as_view(), name='btn-all'),
]