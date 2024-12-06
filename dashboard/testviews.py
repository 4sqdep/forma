from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Exists, OuterRef, Prefetch
from rest_framework import status
from .models import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton

class DashboardButtonListView(APIView):
    def get(self, request, *args, **kwargs):
        response_data = []

        for button in DashboardButton.objects.prefetch_related('dashboardcategorybutton_set'):
            categories_data = []
            button_has_data = False

            for category in button.dashboardcategorybutton_set.all():
                # Har bir kategoriya uchun subkategoriyalarni olish
                subcategories = category.dashboardsubcategorybutton_set.all()

                # Agar subkategoriyalar bo'lsa, has_data=True bo'ladi
                category_has_data = len(subcategories) > 0

                # Agar kategoriya bo'lsa va subkategoriyalar mavjud bo'lsa, button_has_data=True bo'ladi
                if category_has_data:
                    button_has_data = True

                # Kategoriya va subkategoriyalarni response_data ga qo'shish
                categories_data.append({
                    "id": category.id,
                    "name": category.name,
                    "has_data": category_has_data,
                    "subcategories": [
                        {"id": sub.id, "name": sub.name} for sub in subcategories
                    ]
                })

            # Har bir button uchun response_data ni to'ldirish
            response_data.append({
                "id": button.id,
                "name": button.name,
                "has_data": button_has_data,  # Bu yerda button_has_data qiymatini to'g'ri o'rnatish
                "categories": categories_data
            })

        return Response(response_data, status=status.HTTP_200_OK)
