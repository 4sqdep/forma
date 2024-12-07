from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from .models import DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton, ProjectDocumentation
from .serializers import (DashboardButtonSerializer, DashboardCategoryButtonSerializer, ProjectDocumentationSerializer,
                          DashboardSubCategoryButtonSerializer)


class DashboardButtonAPIView(APIView):
    """Asosiy button larni olish uchun View"""
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        btn = DashboardButton.objects.all()
        has_data = btn.exists()
        serializer = DashboardButtonSerializer(btn, many=True)
        return Response({"has_data": has_data, 'data': serializer.data}, status=status.HTTP_200_OK)


class DashboardCategoryButtonAPIView(APIView):
    """Kategoriya button larni olish uchun View"""
    permissions_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        btn = (DashboardCategoryButton.objects.filter(dashboard_button_id=pk)
               .select_related('dashboard_button'))
        has_data = btn.exists()
        serializer = DashboardCategoryButtonSerializer(btn, many=True)
        return Response({"has_data": has_data, 'message': "Kategoriya buttonlar.....", 'data': serializer.data},
                        status=status.HTTP_200_OK)

    """Sub kategoriya button kiritish uchun POST method"""

    def post(self, request):
        serializer = DashboardSubCategoryButtonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': "SubCategory o'zgartirildi....", 'data': serializer.data},
                                status=status.HTTP_200_OK)


class DashboardSubCategoryButtonAPIView(APIView):
    """Sub kategoriya button larni olish uchun View"""
    permissions_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        sub_btn = (DashboardSubCategoryButton.objects.filter(dashboard_category_btn_id=pk)
                   .select_related('dashboard_category_btn'))
        has_data = sub_btn.exists()
        serializer = DashboardSubCategoryButtonSerializer(sub_btn, many=True)
        return Response({"has_data": has_data, 'message': "SubCategory buttonlar.....", 'data': serializer.data},
                        status=status.HTTP_200_OK)


class ProjectDocumentAPIView(APIView):
    """Subkategoriya buttonga tegishli lo'yiha bo'limlarin olish"""
    permissions_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        sub_btn = ProjectDocumentation.objects.filter(subcategories_btn=pk)
        print("EEEEEEE====", sub_btn)
        serializer = ProjectDocumentationSerializer(sub_btn, many=True)
        return Response({'message': "Lo'yiha bo'limlari...", 'data': serializer.data}, status=status.HTTP_200_OK)

