from django.urls import path
from ..views import user


app_name = "account"


urlpatterns = [
    path(
        'register/', 
        user.user_register_api_view, 
        name='register'
    ),
    path(
        'login/', 
        user.user_login_api_view, 
        name='login'
    ),
    path(
        'profile/<int:pk>/', 
        user.user_profile_api_view, 
        name='profile'
    ),
    path(
        'user-all-list/', 
        user.all_user_api_view, 
        name='user-all-list'
    ),
    path(
        '<int:pk>/delete/',
        user.user_delete_api_view,
        name='delete'
    )
]