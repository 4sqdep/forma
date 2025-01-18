from main.apps.dashboard.models.document import NextStageDocuments, ProjectDocumentation
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .utils_serializers import ProjectDocumentationSerializer
from collections import defaultdict
from django.db.models import Count, Case, When, Value, IntegerField
from main.apps.main.models import ObjectsPassword
from main.apps.main.serializers import GetObjectsPasswordSerializer, NextStageDocumentsSerializer
from main.apps.dashboard.models.document import  NextStageDocuments


class NestedDataAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """Navbar menu uchun """
    def get(self, request):
        query_params = request.query_params.get("query")
        try:
            if query_params == '1':
                project_docs = ObjectsPassword.objects.filter(project_documentation__is_obj_password=True)
                serialializer = GetObjectsPasswordSerializer(project_docs, many=True)
                return Response({"message": "Malumotlar......", "data": serialializer.data}, status=status.HTTP_200_OK)
            elif query_params == '2':
                project_docs = NextStageDocuments.objects.filter(project_document__is_project_doc=True)
                serialializer = NextStageDocumentsSerializer(project_docs, many=True)
                return Response({"message": "Malumotlar......", "data": serialializer.data}, status=status.HTTP_200_OK)
            elif query_params == '3':
                project_docs = NextStageDocuments.objects.filter(project_document__is_work_smr=True)
                serialializer = NextStageDocumentsSerializer(project_docs, many=True)
                return Response({"message": "Malumotlar......", "data": serialializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"data": "XATO"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class ProjectDocumentationView(APIView):
#     """Navbar menu uchun """
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         query_params = request.query_params.get('query')
#         try:
#             if query_params == "1":
#                 project_doc = ProjectDocumentation.objects.filter(is_obj_password=True)
#                 next_stage_doc = (NextStageDocuments.objects.filter(project_document__in=project_doc).
#                                   prefetch_related('documents'))
#                 serializer = ProjectDocumentationSerializer(next_stage_doc, many=True)
#                 return Response({"message": "Barcha malumotlar....", "data": serializer.data},
#                                 status=status.HTTP_200_OK)
#             elif query_params == "2":
#                 project_doc = ProjectDocumentation.objects.filter(is_project_doc=True)
#                 next_stage_doc = (NextStageDocuments.objects.filter(project_document__in=project_doc).
#                                   prefetch_related('documents'))
#                 serializer = ProjectDocumentationSerializer(next_stage_doc, many=True)
#                 return Response({"message": "Barcha malumotlar....", "data": serializer.data},
#                                 status=status.HTTP_200_OK)
#             elif query_params == "3":
#                 project_doc = ProjectDocumentation.objects.filter(is_work_smr=True)
#                 next_stage_doc = (NextStageDocuments.objects.filter(project_document__in=project_doc).
#                                   prefetch_related('documents'))
#                 serializer = ProjectDocumentationSerializer(next_stage_doc, many=True)
#                 return Response({"message": "Barcha malumotlar....", "data": serializer.data},
#                                 status=status.HTTP_200_OK)
#             elif query_params == "4":
#                 project_doc = ProjectDocumentation.objects.filter(is_equipment=True)
#                 next_stage_doc = (NextStageDocuments.objects.filter(project_document__in=project_doc).
#                                   prefetch_related('documents'))
#                 serializer = ProjectDocumentationSerializer(next_stage_doc, many=True)
#                 return Response({"message": "Barcha malumotlar....", "data": serializer.data},
#                                 status=status.HTTP_200_OK)
#             else:
#                 return Response(
#                     {"message": "Parametr noto‘g‘ri yoki ma’lumotlar topilmadi"},
#                     status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
