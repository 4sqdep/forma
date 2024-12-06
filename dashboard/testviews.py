from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Exists, OuterRef, Prefetch
from rest_framework import status
from .models import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton

class DashboardButtonListView(APIView):
    def get(self, request, *args, **kwargs):
        # Kategoriyalarga subkategoriyalarni oldindan yuklash
        categories_with_subcategories = DashboardCategoryButton.objects.prefetch_related(
            Prefetch(
                'dashboardsubcategorybutton_set',
                queryset=DashboardSubCategoryButton.objects.all(),
                to_attr='subcategories'
            )
        ).annotate(
            has_data=Exists(
                DashboardSubCategoryButton.objects.filter(
                    dashboard_category_btn=OuterRef('pk')
                )
            )
        )

        response_data = []

        # Har bir tugma uchun ma'lumotlarni yig'ish
        for button in DashboardButton.objects.all():
            categories = categories_with_subcategories.filter(dashboard_button=button)
            categories_data = []
            button_has_data = False

            for category in categories:
                subcategories = category.subcategories
                category_has_data = len(subcategories) > 0

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

            # Tugma darajasidagi ma'lumotlar
            response_data.append({
                "id": button.id,
                "name": button.name,
                "has_data": button_has_data,
                "categories": categories_data
            })

        return Response(response_data, status=status.HTTP_200_OK)
