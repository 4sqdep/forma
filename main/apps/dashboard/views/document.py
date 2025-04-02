# from main.apps.dashboard.models.dashboard import ObjectCategory, Object
# from main.apps.dashboard.models.document import DocumentFiles, NextStageDocuments, ProjectSections
# from main.apps.dashboard.serializers import document as document_serializer
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import permissions, status
# from rest_framework.permissions import IsAuthenticated
# from django.db.models import Q
# from django.db.models import Case, When, Value, BooleanField
# from main.apps.common.pagination import CustomPagination
# from main.apps.main.serializer.statistic import ObjectCategoryStatisticsSerializer
# from django.db.models import Prefetch
# from rest_framework_simplejwt import authentication
# from rest_framework import generics, status, permissions 
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from django.utils.dateparse import parse_date



# class NextStageDocumentsCreateAPIView(generics.CreateAPIView):
#     queryset = NextStageDocuments.objects.all()
#     serializer_class = document_serializer.NextStageDocumentsCreateSerializer
#     authentication_classes = [authentication.JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(created_by=request.user)
#             return Response(
#                 {"message": "Kerakli hujjatlar yaratildi", "data": serializer.data},
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(
#             {"message": "Hujjat yaratishda xatolik yuz berdi", "errors": serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST
#         )

# next_stage_document_create_api_view = NextStageDocumentsCreateAPIView.as_view()


# class NextStageDocumentsListAPIView(generics.ListAPIView):
#     serializer_class = document_serializer.NextStageDocumentsSerializer
#     authentication_classes = [authentication.JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter("p", openapi.IN_QUERY, description="Pagination parameter", type=openapi.TYPE_STRING),
#             openapi.Parameter("is_forma", openapi.IN_QUERY, description="Filter by is_forma", type=openapi.TYPE_BOOLEAN),
#             openapi.Parameter("is_section", openapi.IN_QUERY, description="Filter by is_section", type=openapi.TYPE_BOOLEAN),
#             openapi.Parameter("is_file", openapi.IN_QUERY, description="Filter by is_file", type=openapi.TYPE_BOOLEAN),
#         ]
#     )

#     def get_queryset(self):
#         queryset = NextStageDocuments.objects.all()
#         object = self.kwargs.get("object")  
#         search = self.request.query_params.get("search")
#         is_forma = self.request.query_params.get("is_forma")
#         is_section = self.request.query_params.get("is_section")
#         is_file = self.request.query_params.get("is_file")
#         new = self.request.query_params.get('new')
#         old = self.request.query_params.get('old')
#         start_date = self.request.query_params.get('start_date')
#         end_date = self.request.query_params.get('end_date')

#         if object:
#             queryset = queryset.filter(object_id=object)

#         if search:
#             queryset = queryset.filter(name__icontains=search)
#         if is_forma:
#             queryset = queryset.filter(is_forma=is_forma.lower() in ["true", "1"])
#         if is_section:
#             queryset = queryset.filter(is_section=is_section.lower() in ["true", "1"])
#         if is_file:
#             queryset = queryset.filter(is_file=is_file.lower() in ["true", "1"])
        
#         if start_date:
#             queryset = queryset.filter(created_at__date__gte=start_date)

#         if end_date:
#             queryset = queryset.filter(created_at__date__lte=end_date)

#         if new and new.lower() == 'true':
#             queryset = queryset.order_by('-created_at')

#         if old and old.lower() == 'true':
#             queryset = queryset.order_by('created_at')

#         return queryset
    
#     def get_pagination_class(self):
#         p = self.request.query_params.get("p")
#         if p:
#             return CustomPagination
#         return None

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         paginator_class = self.get_pagination_class()

#         if paginator_class:
#             paginator = paginator_class()
#             page = paginator.paginate_queryset(queryset, request)
#             serializer = self.get_serializer(page, many=True)
#             response_data = paginator.get_paginated_response(serializer.data)
#             response_data.data["status_code"] = status.HTTP_200_OK
#             response_data.data["data"] = response_data.data.pop("results", [])
#             return Response(response_data.data, status=status.HTTP_200_OK)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)

# next_stage_document_list_api_view = NextStageDocumentsListAPIView.as_view()


# class NextStageDocumentsDetailAPIView(generics.RetrieveAPIView):
#     queryset = NextStageDocuments.objects.all()
#     serializer_class = document_serializer.NextStageDocumentsSerializer
#     authentication_classes = [authentication.JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response({"data": serializer.data, "status_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)

# next_stage_document_detail_api_view = NextStageDocumentsDetailAPIView.as_view()


# class NextStageDocumentsUpdateAPIView(generics.UpdateAPIView):
#     queryset = NextStageDocuments.objects.all()
#     serializer_class = document_serializer.NextStageDocumentsCreateSerializer
#     authentication_classes = [authentication.JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"data": serializer.data, "message": "Hujjat muvaffaqiyatli yangilandi", "status_code": status.HTTP_200_OK},
#                 status=status.HTTP_200_OK
#             )
#         return Response({"message": "Hujjatni yangilashda xatolik yuz berdi", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# next_stage_document_update_api_view = NextStageDocumentsUpdateAPIView.as_view()


# class NextStageDocumentsDeleteAPIView(generics.DestroyAPIView):
#     queryset = NextStageDocuments.objects.all()
#     serializer_class = document_serializer.NextStageDocumentsSerializer
#     authentication_classes = [authentication.JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(
#             {"message": "Hujjat muvaffaqiyatli o'chirildi", "status_code": status.HTTP_204_NO_CONTENT},
#             status=status.HTTP_204_NO_CONTENT
#         )

# next_stage_document_delete_api_view = NextStageDocumentsDeleteAPIView.as_view()



# class DocumentFilesCreateAPIView(generics.CreateAPIView):
#     queryset = DocumentFiles.objects.all()
#     serializer_class = document_serializer.FilesSerializer
#     authentication_classes = [authentication.JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "File successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)
#         return Response({"message": "Error creating file", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# file_create_api_view = DocumentFilesCreateAPIView.as_view()


# class DocumentFilesListAPIView(generics.ListAPIView):
#     serializer_class = document_serializer.FilesSerializer
#     authentication_classes = [authentication.JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter("document", openapi.IN_QUERY, description="Filter by document ID", type=openapi.TYPE_INTEGER),
#             openapi.Parameter("name", openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
#             openapi.Parameter("file_code", openapi.IN_QUERY, description="Filter by file code", type=openapi.TYPE_STRING),
#         ]
#     )
#     def get_queryset(self):
#         document = self.kwargs.get("document") 
#         queryset = DocumentFiles.objects.all()
#         project_section = self.request.query_params.get("project_section")
#         name = self.request.query_params.get("name")
#         file_code = self.request.query_params.get("file_code")
#         start_date = self.request.query_params.get('start_date')
#         end_date = self.request.query_params.get('end_date')

#         if document:
#             queryset = queryset.filter(document=document)
        
#         if project_section:
#             queryset = queryset.filter(project_section=project_section)
#         if name:
#             queryset = queryset.filter(name__icontains=name)
#         if file_code:
#             queryset = queryset.filter(file_code__icontains=file_code)
        
#         if start_date and end_date:
#             queryset = queryset.filter(calendar__range=[start_date, end_date])

#         elif start_date:
#             queryset = queryset.filter(calendar=start_date)

#         return queryset
    
#     def get_pagination_class(self):
#         p = self.request.query_params.get('p')
#         if p:
#             return CustomPagination
#         return None

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         paginator_class = self.get_pagination_class()

#         if paginator_class:
#             paginator = paginator_class()
#             page = paginator.paginate_queryset(queryset, request)
#             serializer = self.get_serializer(page, many=True)
#             response_data = paginator.get_paginated_response(serializer.data)
#             response_data.data["status_code"] = status.HTTP_200_OK
#             response_data.data["data"] = response_data.data.pop("results", [])
#             return Response(response_data.data, status=status.HTTP_200_OK)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)

# file_list_api_view = DocumentFilesListAPIView.as_view()


# class DocumentFilesDetailAPIView(generics.RetrieveAPIView):
#     queryset = DocumentFiles.objects.all()
#     serializer_class = document_serializer.FilesSerializer
#     authentication_classes = [authentication.JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response({"data": serializer.data, "status_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)

# file_detail_api_view = DocumentFilesDetailAPIView.as_view()


# class DocumentFilesUpdateAPIView(generics.UpdateAPIView):
#     queryset = DocumentFiles.objects.all()
#     serializer_class = document_serializer.FilesSerializer
#     authentication_classes = [authentication.JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"data": serializer.data, "message": "File successfully updated", "status_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
#         return Response({"message": "Error updating file", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# file_update_api_view = DocumentFilesUpdateAPIView.as_view()


# class DocumentFilesDeleteAPIView(generics.DestroyAPIView):
#     queryset = DocumentFiles.objects.all()
#     serializer_class = document_serializer.FilesSerializer
#     authentication_classes = [authentication.JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response({"message": "File successfully deleted", "status_code": status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)

# file_delete_api_view = DocumentFilesDeleteAPIView.as_view()



# class ProjectSectionsAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk=None):
#         try:
#             sections = ProjectSections.objects.filter(next_stage_documents_id=pk)
#             if not sections.exists():
#                 return Response(
#                     {"message": "Bo'limlar topilmadi."},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             paginator = CustomPagination()
#             paginated_queryset = paginator.paginate_queryset(sections, request)
#             serializer = document_serializer.ProjectSectionsSerializer(paginated_queryset, many=True)

#             return Response(
#                 {
#                     "message": "Barcha bo'limlar muvaffaqiyatli olindi",
#                     "total": sections.count(),
#                     "sections": serializer.data
#                 },
#                 status=status.HTTP_200_OK
#             )
#         except Exception as e:
#             return Response(
#                 {"message": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#     def post(self, request):
#         serializer = document_serializer.CreateProjectSectionsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(created_by=request.user)
#             return Response({
#                 'message':"Bo'lim muvaffaqiyatli yaratildi",
#                 'data': serializer.data,},
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             data={"message": "Xatolik yuz berdi.", "errors": serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def patch(self, request, pk=None):
#         try:
#             section = ProjectSections.objects.get(id=pk)
#         except ProjectSections.DoesNotExist:
#             return Response(
#                 {"message": "Bo'lim topilmadi."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         new_name = request.data.get('name')
#         if not new_name:
#             return Response(
#                 {"message": "Name maydonini kiritish shart"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         section.name = new_name
#         section.save()

#         return Response(
#             {"message": "Nomi muvaffaqiyatli yangilandi", "name": section.name},
#             status=status.HTTP_200_OK
#         )

#     def delete(self, request, pk=None):
#         try:
#             section = ProjectSections.objects.get(id=pk)
#             section.delete()
#             return Response(
#                 {"message": "Bo'lim muvaffaqiyatli o'chirildi."},
#                 status=status.HTTP_204_NO_CONTENT
#             )
#         except ProjectSections.DoesNotExist:
#             return Response(
#                 {"message": "Bo'lim topilmadi."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

# project_section_api_view = ProjectSectionsAPIView.as_view()



# class MultipleFileUploadView(APIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         serializer = document_serializer.MultipleFileUploadSerializer(
#             data=request.data, context={"request": request}
#         )
#         if serializer.is_valid():
#             uploaded_files = serializer.save()  
#             response_serializer = document_serializer.FilesSerializer(uploaded_files, many=True)  
#             return Response(
#                 data=response_serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
#         return Response({'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# multiple_file_upload_api_view = MultipleFileUploadView.as_view()



# class GetFilesAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     def get(self, request, pk=None):
#         try:
#             files = DocumentFiles.objects.filter(document_id=pk)
#             if not files.exists():
#                 return Response(
#                     data={"message": "Tegishli fayllar topilmadi"},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             paginator = CustomPagination()
#             paginated_queryset = paginator.paginate_queryset(files, request)
#             serializer = document_serializer.GetFilesSerializer(paginated_queryset, many=True)
            
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_200_OK
#             )

#         except Exception as e:
#             return Response(
#                 data={"message": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

# get_files_api_view = GetFilesAPIView.as_view()



# class GetFilesSectionAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     def get(self, request, pk=None):
#         try:
#             files = DocumentFiles.objects.filter(project_section_id=pk)
#             if not files.exists():
#                 return Response(
#                     data={"message": "Tegishli fayllar topilmadi"},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             paginator = CustomPagination()
#             paginated_queryset = paginator.paginate_queryset(files, request)
#             serializer = document_serializer.GetFilesSerializer(paginated_queryset, many=True)

#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_200_OK
#             )

#         except Exception as e:
#             return Response(
#                 data={"message": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

# get_files_section_api_view = GetFilesSectionAPIView.as_view()



# class FilesSearchAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         document_id = request.query_params.get('document_id')
#         project_section_id = request.query_params.get('project_section_id')
#         search_query = request.query_params.get('query')

#         if not search_query:
#             return Response(
#                 data={"message": "Qidiruv so'rovi (query) parametri talab qilinadi."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if document_id:
#             files = DocumentFiles.objects.filter(
#                 Q(document_id=document_id) & (
#                     Q(name__icontains=search_query) |
#                     Q(calendar__icontains=search_query) |
#                     Q(file_code__icontains=search_query)
#                 )
#             )
#         elif project_section_id:
#             files = DocumentFiles.objects.filter(
#                 Q(project_section_id=project_section_id) & (
#                     Q(name__icontains=search_query) |
#                     Q(calendar__icontains=search_query) |
#                     Q(file_code__icontains=search_query)
#                 )
#             )
#         else:
#             return Response(
#                 data={"message": "Document_id yoki project_section_idni kiritishingiz kerak."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if not files.exists():
#             return Response(
#                 data={"message": "Mos keluvchi fayllar topilmadi."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         paginator = CustomPagination()
#         paginated_queryset = paginator.paginate_queryset(files, request)
#         result = paginated_queryset.values('name', 'files', 'file_code', 'calendar', 'created_at')
#         return Response(
#             data=list(result),
#             status=status.HTTP_200_OK
#         )

# file_search_api_view = FilesSearchAPIView.as_view()




# class AllStatisticsData(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         all_statistics = ObjectCategory.objects.only("id", "name")
#         if not all_statistics.exists():
#             return Response(
#                 data={"message": "Statistik ma'lumotlar topilmadi."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = ObjectCategoryStatisticsSerializer(all_statistics, many=True)
        
#         formatted_data = {
#             item['name'].lower().replace(" ", "_"): item
#             for item in serializer.data
#         }
#         return Response({'data':formatted_data}, status=status.HTTP_200_OK)

# all_statistics_data_api_view = AllStatisticsData.as_view()
