from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
from .models import PrimaryFiles, PrimaryDocuments, ObjectName
from account.models import User



class PrimaryDocumentAPIView(APIView):
    """Loyihachi birlamchi hujjat va fayllarni kiritish uchun view"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    pass