from django.urls import path
from .views import RegisterUser, LoginUser


app_name = "account"

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
]