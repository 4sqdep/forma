from django.urls import path
from .views import RegisterUser, LoginUser, UserProfileAPIView


app_name = "account"

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='profile'),
]