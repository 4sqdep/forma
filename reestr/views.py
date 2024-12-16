import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage
from .models import Nocapitelni
from rest_framework import status


class NocapitelniExcelToJsonView(APIView):
    def get(self, request, *args, **kwargs):
        # Faylni modeldan olish
        try:
            nocapitelni_instance = Nocapitelni.objects.first()  # Eng birinchi faylni oladi
            if not nocapitelni_instance or not nocapitelni_instance.file:
                return Response({"error": "Fayl topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

            file_path = nocapitelni_instance.file.path  # Faylning to‘liq yo‘lini olish

            # Excel faylni JSON formatga o‘tkazish
            df = pd.read_excel(file_path)  # Excel faylni o‘qish
            data = df.to_dict(orient='records')  # JSON formatga aylantirish

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)