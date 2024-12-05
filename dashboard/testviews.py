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
            button_has_data = False  # DashboardButton darajasida umumiy flag

            for category in categories:
                subcategories = category.dashboardsubcategorybutton_set.all()
                category_has_data = subcategories.exists()  # Subkategoriya mavjudligini tekshirish

                # Agar subkategoriya mavjud bo'lsa, has_data=True bo'lishi kerak
                if category_has_data:
                    button_has_data = True

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

            # Tugmalar ma'lumotlari
            response_data.append({
                "id": button.id,
                "name": button.name,
                "has_data": button_has_data,
                "categories": categories_data
            })

        return Response(response_data, status=status.HTTP_200_OK)

