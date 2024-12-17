from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from .models import (DashboardButton, DashboardCategoryButton, DashboardSubCategoryButton,
                     ProjectDocumentation, NextStageDocuments, Files)
from .serializers import (DashboardButtonSerializer, DashboardCategoryButtonSerializer, ProjectDocumentationSerializer,
                          DashboardSubCategoryButtonSerializer, NextStageDocumentsSerializer,
                          NextStageDocumentsCreateSerializer, FilesSerializer, MultipleFileUploadSerializer,
                          GetFilesSerializer)


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

    def patch(self, request, pk=None):
        try:
            document = NextStageDocuments.objects.get(pk=pk)
        except NextStageDocuments.DoesNotExist:
            return Response({'error': "Bu idda dokument nomi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        new_name = request.data.get('name')
        if not new_name:
            return Response({'message': "Name maydonini kiritish shart"}, status=status.HTTP_400_BAD_REQUEST)
        document.name = new_name
        document.save()
        return Response({"message": "Name muvaffaqiyatli yangilandi", "data": document.name}, status=status.HTTP_200_OK)


class MultipleFileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        serializer = MultipleFileUploadSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            uploaded_files = serializer.save()  # Fayllarni saqlash
            response_serializer = FilesSerializer(uploaded_files, many=True)  # Javobni formatlash
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetFilesAPIView(APIView):
    permissions_classes = [IsAuthenticated]
    multipart_parser_classes = [MultiPartParser, FormParser]
    def get(self, request, pk=None):
        try:
            files = Files.objects.filter(document_id=pk)
            if not files.exists():
                return Response({'message': "Tegishli fayllar topilmadi"}, status=status.HTTP_404_NOT_FOUND)
            serializer = GetFilesSerializer(files, many=True)
            return Response({'message': "Barcha fayllar", 'data': serializer.data}, status=status.HTTP_200_OK)
        except Files.DoesNotExist as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
