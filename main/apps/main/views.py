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
from ..common.response import (
    PostResponse, 
    ErrorResponse,
    PutResponse, 
    ListResponse, 
    DestroyResponse
)



class GetObjectsPasswordView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, pk=None):
        project_doc = ObjectsPassword.objects.filter(project_documentation_id=pk)
        serializer = GetObjectsPasswordSerializer(project_doc, many=True)
        return ListResponse(data=serializer.data, message="Barcha malumotlar")

    def post(self, request):
        serializer = CreateObjectsPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return PostResponse(data=serializer.data, message="Malumot qo'shildi")
        return ErrorResponse(message="Malumot qo'shilmadi", errors=serializer.errors, status_code=400)

    def patch(self, request, pk=None):
        try:
            obj_password = ObjectsPassword.objects.get(id=pk)
        except ObjectsPassword.DoesNotExist:
            return ErrorResponse(message="Obyekt topilmadi", status_code=404)

        serializer = PatchbjectsPasswordSerializer(obj_password, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return PutResponse(data=serializer.data, message="Malumot yangilandi")
        return ErrorResponse(message="Malumotni yangilashda xatolik", errors=serializer.errors, status_code=400)

get_object_password_api_view = GetObjectsPasswordView.as_view()
        


class UploadFilesAPIView(APIView):
    permission_classes = [IsAuthenticated]  
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = FilesCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return PostResponse(data=serializer.data, message="Fayl muvaffaqiyatli yuklandi")
        return ErrorResponse(message="Yuklashda xatolik yuz berdi", errors=serializer.errors, status_code=400)

upload_files_api_view = UploadFilesAPIView.as_view()



class GetFilesAPIView(APIView):
    permission_classes = [IsAuthenticated]  
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk=None):
        get_files = Files.objects.filter(obj_password_id=pk)
        serializer = GetFilesSerializer(get_files, many=True)
        return ListResponse(data=serializer.data, message="Fayllar topildi")

get_files_api_view = GetFilesAPIView.as_view()



class SearchObjectsNameAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        q = request.query_params.get('query')
        if not q:
            return ErrorResponse(message="Qidiruv so'rovi (query) parametri talab qilinadi.", status_code=400)
        obj_name = Object.objects.filter(Q(name__icontains=q))
        serializer = SearchObjectsNameSerializer(obj_name, many=True)
        return ListResponse(data=serializer.data, message="Siz izlagan ma'lumotlar")

search_object_name_api_view = SearchObjectsNameAPIView.as_view()