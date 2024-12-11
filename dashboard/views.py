from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from .models import (DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton,
                     ProjectDocumentation, NextStageDocuments, Files)
from .serializers import (DashboardButtonSerializer, DashboardCategoryButtonSerializer, ProjectDocumentationSerializer,
                          DashboardSubCategoryButtonSerializer, NextStageDocumentsSerializer,
                          NextStageDocumentsCreateSerializer, FilesSerializer)


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


class NextStageDocumentsAPIView(APIView):
    """ProjectDocument ga tegishli loyiha asosiy bo'limlarini olish uchun"""
    permissions_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        projects = NextStageDocuments.objects.filter(project_document_id=pk)
        serializer = NextStageDocumentsSerializer(projects, many=True)
        return Response({'message': "SuccessFull....", 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        serializer = NextStageDocumentsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': "Kerakli papkalar yaratildi....", 'data': serializer.data},
                            status=status.HTTP_201_CREATED)


class FilesCreateAPIView(APIView):
    """Keyingi hujjatlar modeliga fayllarni yuklash uchun """
    permissions_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        document_id = request.data.get('document_id')
        # Tekshiramiz: NextStageDocuments modeli mavjudmi?
        try:
            document = NextStageDocuments.objects.get(id=document_id)
        except NextStageDocuments.DoesNotExist:
            return Response({"error": "NextStageDocuments topilmadi."}, status=status.HTTP_404_NOT_FOUND)


        # Fayllarni yuklash uchun
        files = request.FILES.getlist('files')
        if not files:
            return Response({"error": "Hech qanday fayl taqdim etilmaydi."}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_files = []
        for file in files:
            file_instance = Files.objects.bulk_create(
                document=document,
                user=request.user,  # Hozirgi foydalanuvchini biriktiramiz
                files=file
            )
            uploaded_files.append(file_instance)

        # Serializatsiya qilingan ma'lumotlarni qaytarish
        serializer = FilesSerializer(uploaded_files, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
