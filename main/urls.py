from django.urls import path
from .views import PostList
from .designer import ObjectNameAPIView


app_name = 'main'

urlpatterns = [
    path('post/', PostList.as_view(), name='post-list'),
    path('get-object-list/', ObjectNameAPIView.as_view(), name='get-object-list'),
]