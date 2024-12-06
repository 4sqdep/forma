from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Exists, OuterRef, Prefetch, Subquery
from rest_framework import status
from .models import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton


class DashboardButtonListView(APIView):
    def get(self, request, *args, **kwargs):
        buttons_with_categories = DashboardButton.objects.prefetch_related(
            'dashboardcategorybutton_set',
            queryset=DashboardCategoryButton.objects.annotate(
                has_data=Subquery(
                    DashboardSubCategoryButton.objects.filter(
                        dashboard_category_btn=OuterRef('pk')
                    ).exists()
                )
            ).prefetch_related(
                'subcategories',
                queryset=DashboardSubCategoryButton.objects.all()
            )
        )

        response_data = []
        for button in buttons_with_categories:
            categories_data = []
            for category in button.dashboardcategorybutton_set.all():
                categories_data.append({
                    "id": category.id,
                    "name": category.name,
                    "has_data": category.has_data or len(category.subcategories) > 0,
                    "subcategories": [
                        {"id": sub.id, "name": sub.name} for sub in category.subcategories
                    ]
                })
            response_data.append({
                "id": button.id,
                "name": button.name,
                "has_data": any(category['has_data'] for category in categories_data),
                "categories": categories_data
            })

        return Response(response_data, status=status.HTTP_200_OK)