from main.apps.dashboard.models.dashboard import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton
from main.apps.dashboard.serializers.dashboard import DashboardButtonSerializer, DashboardCategoryButtonSerializer, DashboardSubCategoryButtonSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Case, When, Value, BooleanField


class DashboardButtonAPIView(APIView):
    """Asosiy button larni olish uchun View"""
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        btn = DashboardButton.objects.annotate(
            category_count=Count('dashboardcategorybutton'),  # Kategoriya sonini hisoblash
            has_data=Case(
                When(category_count__gt=0, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )  # Kategoriya mavjudligini aniqlash
        )
        serializer = DashboardButtonSerializer(btn, many=True)
        return Response({'message': 'Asosiy button', 'data': serializer.data}, status=status.HTTP_200_OK)

dashboard_button_api_view = DashboardButtonAPIView.as_view()



class DashboardCategoryButtonAPIView(APIView):
    """Kategoriya button larni olish uchun View"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            btn = (
                DashboardCategoryButton.objects.filter(dashboard_button_id=pk)
                .select_related('dashboard_button')  # Bog‘liq ma'lumotlarni yuklash
                .annotate(
                    subcategory_count=Count('dashboardsubcategorybutton', distinct=True),  # Subkategoriyalarni sanash
                    has_data=Case(
                        When(subcategory_count__gt=0, then=Value(True)),  # Agar subkategoriya mavjud bo‘lsa
                        default=Value(False),
                        output_field=BooleanField()
                    )))

            # Serializatsiya qilish
            serializer = DashboardCategoryButtonSerializer(btn, many=True)
            return Response({'message': "Kategoriya buttonlar.....", 'data': serializer.data},
                status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": f"Xatolik yuz berdi: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    """Sub kategoriya button kiritish uchun POST method"""

    def post(self, request):
        serializer = DashboardSubCategoryButtonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': "SubCategory o'zgartirildi....", 'data': serializer.data},
                                status=status.HTTP_200_OK)

dashboard_category_button_api_view = DashboardCategoryButtonAPIView.as_view()



class DashboardSubCategoryButtonAPIView(APIView):
    """Sub kategoriya button larni olish uchun View"""
    permissions_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        sub_btn = (DashboardSubCategoryButton.objects.filter(dashboard_category_btn_id=pk).select_related('dashboard_category_btn'))
        serializer = DashboardSubCategoryButtonSerializer(sub_btn, many=True)
        return Response({'message': "SubCategory buttonlar.....", 'data': serializer.data},
                        status=status.HTTP_200_OK)

dashboard_subcategory_button_api_view = DashboardSubCategoryButtonAPIView.as_view()
