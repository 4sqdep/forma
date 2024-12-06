from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Exists, OuterRef
from rest_framework import status
from .models import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton

class DashboardButtonListView(APIView):
    def get(self, request, *args, **kwargs):
        # Subkategoriya mavjudligini aniqlash uchun `Exists`dan foydalanamiz
        subcategory_exists = DashboardSubCategoryButton.objects.filter(
            dashboard_category_btn=OuterRef('pk')
        )

        # Har bir kategoriya uchun subkategoriya mavjudligini aniqlash
        categories_with_data = DashboardCategoryButton.objects.annotate(
            has_data=Exists(subcategory_exists)
        )

        # Har bir tugma uchun ma'lumotlarni qayta ishlash
        response_data = []
        for button in DashboardButton.objects.all():
            button_categories = categories_with_data.filter(dashboard_button=button)
            # Tugma darajasida subkategoriya mavjudligini aniqlash
            button_has_data = button_categories.filter(has_data=True).exists()

            categories_data = []
            for category in button_categories:
                subcategories = DashboardSubCategoryButton.objects.filter(
                    dashboard_category_btn=category
                )

                categories_data.append({
                    "id": category.id,
                    "name": category.name,
                    "has_data": category.has_data,  # Annotated qiymat
                    "subcategories": [
                        {
                            "id": sub.id,
                            "name": sub.name,
                        } for sub in subcategories
                    ]
                })

            # Tugma ma'lumotlari
            response_data.append({
                "id": button.id,
                "name": button.name,
                "has_data": button_has_data,
                "categories": categories_data,
            })

        return Response(response_data, status=status.HTTP_200_OK)
