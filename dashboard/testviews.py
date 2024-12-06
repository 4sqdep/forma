from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Exists, OuterRef, Prefetch
from rest_framework import status
from .models import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton

class DashboardButtonListView(APIView):
    def get(self, request, *args, **kwargs):
        # Annotatsiya subquery orqali subkategoriyalarni tekshirish
        subcategory_exists = DashboardSubCategoryButton.objects.filter(
            dashboard_category_btn=OuterRef('pk')
        )

        # Annotatsiya kategoriyalarda subkategoriya borligini aniqlash uchun
        categories_with_subcategories = DashboardCategoryButton.objects.annotate(
            has_data=Exists(subcategory_exists)
        ).prefetch_related(
            Prefetch(
                'dashboardsubcategorybutton_set',
                queryset=DashboardSubCategoryButton.objects.all(),
                to_attr='subcategories'
            )
        )

        response_data = []

        # Har bir asosiy tugma uchun ma'lumotlarni yig'ish
        for button in DashboardButton.objects.prefetch_related('dashboardcategorybutton_set'):
            categories = categories_with_subcategories.filter(dashboard_button=button)
            categories_data = []
            button_has_data = False

            for category in categories:
                subcategories = category.subcategories
                category_has_data = category.has_data or len(subcategories) > 0

                if category_has_data:
                    button_has_data = True

                categories_data.append({
                    "id": category.id,
                    "name": category.name,
                    "has_data": category_has_data,
                    "subcategories": [
                        {"id": sub.id, "name": sub.name} for sub in subcategories
                    ]
                })

            # Asosiy tugma uchun ma'lumot
            response_data.append({
                "id": button.id,
                "name": button.name,
                "has_data": button_has_data,
                "categories": categories_data
            })

        return Response(response_data, status=status.HTTP_200_OK)
