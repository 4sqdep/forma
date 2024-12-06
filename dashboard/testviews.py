from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Exists, OuterRef, Prefetch
from rest_framework import status
from .models import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton

class DashboardButtonListView(APIView):
    def get(self, request, *args, **kwargs):
        response_data = []

        # Loop through each DashboardButton and gather its related categories and subcategories
        for button in DashboardButton.objects.prefetch_related('dashboardcategorybutton_set'):
            categories_data = []
            button_has_data = False

            # Loop through categories associated with the current button
            for category in button.dashboardcategorybutton_set.prefetch_related('dashboardsubcategorybutton_set'):
                # Subcategories for the current category
                subcategories = category.dashboardsubcategorybutton_set.all()
                category_has_data = len(subcategories) > 0

                if category_has_data:
                    button_has_data = True

                # Append the category with its subcategories to the response
                categories_data.append({
                    "id": category.id,
                    "name": category.name,
                    "has_data": category_has_data,
                    "subcategories": [
                        {"id": sub.id, "name": sub.name} for sub in subcategories
                    ]
                })

            # Append the DashboardButton data with its categories
            response_data.append({
                "id": button.id,
                "name": button.name,
                "has_data": button_has_data,
                "categories": categories_data
            })

        return Response(response_data, status=status.HTTP_200_OK)

