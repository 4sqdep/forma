from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DashboardButton
from .testserializers import DashboardButtonSerializer

class DashboardButtonListView(APIView):
    def get(self, request, *args, **kwargs):
        buttons = DashboardButton.objects.all()
        response_data = []

        for button in buttons:
            categories = button.dashboardcategorybutton_set.all()
            categories_data = []
            has_data = False

            for category in categories:
                subcategories = category.dashboardsubcategorybutton_set.all()
                has_subcategory_data = subcategories.exists()
                has_data = has_data or has_subcategory_data

                categories_data.append({
                    "id": category.id,
                    "name": category.name,
                    "has_data": has_subcategory_data,
                    "subcategories": [
                        {
                            "id": sub.id,
                            "name": sub.name,
                        } for sub in subcategories
                    ]
                })

            response_data.append({
                "id": button.id,
                "name": button.name,
                "has_data": has_data,
                "categories": categories_data
            })

        return Response(response_data, status=status.HTTP_200_OK)
