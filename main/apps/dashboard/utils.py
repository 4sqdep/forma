# from main.apps.dashboard.models.dashboard import DashboardSubCategoryButton
# from main.apps.dashboard.models.document import NextStageDocuments, ProjectDocumentation
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import permissions, status
# from rest_framework.permissions import IsAuthenticated
# from django.db.models import Q
# from .utils_serializers import ProjectDocumentationSerializer
# from collections import defaultdict
# from django.db.models import Count, Case, When, Value, IntegerField
# from main.apps.main.models import ObjectsPassword
# from main.apps.main.serializers import (GetObjectsPasswordSerializer, NextStageDocumentsSerializer)
# from main.apps.dashboard.models.document import  NextStageDocuments
# from main.apps.main.serializer.statistic import DashboardButtonStatisticsSerializer
# from main.apps.common.pagination import CustomPagination
# from main.apps.dashboard.models.dashboard import DashboardButton
# from django.db.models import Prefetch



# class NestedDataAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     """Navbar menu uchun """
#     def get(self, request):
#         query_params = request.query_params.get("query")
#         try:
#             if query_params == '1':
#                 project_docs = ObjectsPassword.objects.filter(project_documentation__is_obj_password=True)
#                 paginator = CustomPagination()
#                 paginated_queryset = paginator.paginate_queryset(project_docs, request)
#                 serialializer = GetObjectsPasswordSerializer(paginated_queryset, many=True)
#                 return Response({"message": "Malumotlar......", "data": serialializer.data}, status=status.HTTP_200_OK)
#             elif query_params == '2':
#                 sub_btns = DashboardSubCategoryButton.objects.prefetch_related(
#                     Prefetch(
#                         'nextstagedocuments_set',
#                         queryset=NextStageDocuments.objects.filter(project_document__is_project_doc=True),
#                         to_attr='filtered_docs'
#                     )
#                 )
#                 paginator = CustomPagination()
#                 data = [
#                     {
#                         "sub_btn_id": sub_btn.id,
#                         "sub_btn_title": sub_btn.name,
#                         "project_docs": NextStageDocumentsSerializer(paginator.paginate_queryset(sub_btn.filtered_docs, request), many=True).data
#                     }
#                     for sub_btn in sub_btns
#                 ]
#                 return Response({"projects": data}, status=status.HTTP_200_OK)
#             elif query_params == '3':
#                 project_docs = NextStageDocuments.objects.filter(project_document__is_work_smr=True)
#                 paginator = CustomPagination()
#                 paginated_queryset = paginator.paginate_queryset(project_docs, request)
#                 serialializer = NextStageDocumentsSerializer(paginated_queryset, many=True)
#                 return Response({"message": "Malumotlar......", "data": serialializer.data}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"data": "XATO"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# nested_data_api_view = NestedDataAPIView.as_view()


# class ObjectsPasswordDetailAPIView(APIView):
#     """Obyekt pasporti uchun qilinga deteil"""
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk=None):
#         get_password = ObjectsPassword.objects.filter(subcategory_btn_id=pk)
#         if not get_password.exists():
#             return Response({'message': "Malumot yo'q"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = GetObjectsPasswordSerializer(get_password, many=True)
#         return Response({'message': "Malumotlar......", "data": serializer.data}, status.HTTP_200_OK)



# class StatisticalData(APIView):
#     """Statistik ma'lumotlar olish uchun"""
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         all_statistics = DashboardButton.objects.all()
#         serializer = DashboardButtonStatisticsSerializer(all_statistics, many=True)
#         response_data = {
#             "message": "Statistik ma'lumotlar........",
#             "data": {}
#         }
#         for item in serializer.data:
#             key = item['name'].lower().replace(" ", "_")  
#             response_data["data"][key] = item
#         return Response(response_data, status=status.HTTP_200_OK)








