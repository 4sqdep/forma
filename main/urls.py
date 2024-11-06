from django.urls import path
from .views import PostList


app_name = 'main'

urlpatterns = [
    path('post/', PostList.as_view(), name='post-list'),
]