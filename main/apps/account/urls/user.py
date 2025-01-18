from django.urls import path

from main.apps.account.views.user import LoginUser, RegisterUser, UserProfileAPIView, AllUsersListAPIView



app_name = "account"

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='profile'),
    path('user-all-list/', AllUsersListAPIView.as_view(), name='user-all-list'),
]