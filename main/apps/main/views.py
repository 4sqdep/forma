from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import ObjectsPassword, Files
from .serializers import (
    GetObjectsPasswordSerializer, 
    CreateObjectsPasswordSerializer, 
    GetFilesSerializer,
    FilesCreateSerializer, 
    SearchObjectsNameSerializer, 
    PatchbjectsPasswordSerializer
)
from ..dashboard.models.dashboard import Object
from rest_framework.response import Response
from rest_framework import status



class GetObjectsPasswordView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, pk=None):
        project_doc = ObjectsPassword.objects.filter(project_documentation_id=pk)
        serializer = GetObjectsPasswordSerializer(project_doc, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK, headers={"message": "Barcha malumotlar"})

    def post(self, request):
        serializer = CreateObjectsPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED, headers={"message": "Malumot qo'shildi"})
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST, headers={"message": "Malumot qo'shilmadi"})

    def patch(self, request, pk=None):
        try:
            obj_password = ObjectsPassword.objects.get(id=pk)
        except ObjectsPassword.DoesNotExist:
            return Response(data={"message": "Obyekt topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PatchbjectsPasswordSerializer(obj_password, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK, headers={"message": "Malumot yangilandi"})
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST, headers={"message": "Malumotni yangilashda xatolik"})

get_object_password_api_view = GetObjectsPasswordView.as_view()



class UploadFilesAPIView(APIView):
    permission_classes = [IsAuthenticated]  
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = FilesCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED, headers={"message": "Fayl muvaffaqiyatli yuklandi"})
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST, headers={"message": "Yuklashda xatolik yuz berdi"})

upload_files_api_view = UploadFilesAPIView.as_view()



class GetFilesAPIView(APIView):
    permission_classes = [IsAuthenticated]  
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk=None):
        get_files = Files.objects.filter(obj_password_id=pk)
        serializer = GetFilesSerializer(get_files, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK, headers={"message": "Fayllar topildi"})

get_files_api_view = GetFilesAPIView.as_view()



class SearchObjectsNameAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        q = request.query_params.get('query')
        if not q:
            return Response(data={"message": "Qidiruv so'rovi (query) parametri talab qilinadi."}, status=status.HTTP_400_BAD_REQUEST)

        obj_name = Object.objects.filter(Q(name__icontains=q))
        serializer = SearchObjectsNameSerializer(obj_name, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK, headers={"message": "Siz izlagan ma'lumotlar"})

search_object_name_api_view = SearchObjectsNameAPIView.as_view()
