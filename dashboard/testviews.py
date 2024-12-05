from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DashboardButton

class DashboardButtonListView(APIView):
    def get(self, request, *args, **kwargs):
        buttons = DashboardButton.objects.all()
        response_data = []

        for button in buttons:
            categories = button.dashboardcategorybutton_set.all()
            categories_data = []
            button_has_data = False  # DashboardButton darajasida mavjudlik flagi

            for category in categories:
                subcategories = category.dashboardsubcategorybutton_set.all()
                category_has_data = subcategories.exists()  # Subkategoriya mavjudligi

                # Kategoriya darajasida "has_data" ni yangilash
                if category.name:  # Agar kategoriya nomi mavjud bo‘lsa, uni mavjud deb belgilaymiz
                    category_has_data = True

                button_has_data = button_has_data or category_has_data  # Umumiy flagni yangilash

                categories_data.append({
                    "id": category.id,
                    "name": category.name,
                    "has_data": category_has_data,
                    "subcategories": [
                        {
                            "id": sub.id,
                            "name": sub.name
                        } for sub in subcategories
                    ]
                })

            response_data.append({
                "id": button.id,
                "name": button.name,
                "has_data": button_has_data,
                "categories": categories_data
            })

        return Response(response_data, status=status.HTTP_200_OK)
