from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db.models import Count, Case, When, Value, BooleanField, Subquery, OuterRef
from .models import ObjectsPassword, Files
from .serializers import (GetObjectsPasswordSerializer, CreateObjectsPasswordSerializer, GetFilesSerializer,
                          FilesCreateSerializer)



class GetObjectsPasswordView(APIView):
    """Obyekt pasportini olish"""
    permissions_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        project_doc = ObjectsPassword.objects.filter(project_documentation_id=pk)
        serializer = GetObjectsPasswordSerializer(project_doc, many=True)
        return Response({"message": "Barcha malumotlar....", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """Obyekt pasportini qo'shish"""
        serializer = CreateObjectsPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'message': "Malumot qo'shildi......", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'message': "Malumot qo'shilmadi .. . .", "data": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk=None):
        obj_password = ObjectsPassword.objects.get(id=pk)
        serializer = CreateObjectsPasswordSerializer(obj_password, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'message': "Malumot yangilandi.....", "data": serializer.data},
            status=status.HTTP_200_OK)

class UploadFilesAPIView(APIView):
    """Opyekt pasporti uchun fayl yuklash"""
    permissions_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        serializer = FilesCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({"message": "Fayl yuklandi......", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'message': "Yuklashda xatolik yuzberdi......", "data": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class GetFilesAPIView(APIView):
    """Obyektga tegishli faylni olish uchun"""
    permissions_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request, pk=None):
        get_files = Files.objects.filter(obj_password_id=pk)
        serializer = GetFilesSerializer(get_files, many=True)
        return Response({'message': "Fayl....", "data": serializer.data}, status=status.HTTP_200_OK)