from django.urls import path
from .views import NocapitelniExcelToJsonView


app_name = 'reestr'

urlpatterns = [
    path('get-files/', NocapitelniExcelToJsonView.as_view(), name='get-files'),
]