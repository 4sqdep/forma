from main.apps.dashboard.models.dashboard import ObjectCategory, Object
from main.apps.dashboard.models.document import Files, NextStageDocuments, ProjectSections
from main.apps.dashboard.serializers import document as document_serializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db.models import Case, When, Value, BooleanField
from main.apps.common.pagination import CustomPagination
from main.apps.dashboard.serializers.document import ProjectDocumentationSerializerHas, NextStageDocumentsSerializer
from main.apps.main.models import ObjectsPassword
from main.apps.main.serializer.statistic import ObjectCategoryStatisticsSerializer
from main.apps.main.serializers import GetObjectsPasswordSerializer
from django.db.models import Prefetch
from ...common.response import (
    ListResponse,
    ErrorResponse,
    PutResponse,
    PostResponse,
    DestroyResponse
)




class ProjectDocumentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        order = [
            "Obyekt pasporti",
            "Loyiha hujjatlari",
            "Qurilish montaj ishlari hujjatlari",
            "Uskunalar hujjatlari",
        ]
        order_case = Case(*[
            When(name=name, then=index) for index, name in enumerate(order)
        ])

        try:
            subcategory = Object.objects.get(id=pk)
            sub_btn = subcategory.projectdocumentation.all().order_by(order_case).annotate(
                has_data=Case(
                    When(name__isnull=False, then=Value(True)),  
                    default=Value(False),
                    output_field=BooleanField()
                )
            )
            serializer = ProjectDocumentationSerializerHas(sub_btn, many=True)
            return ListResponse(
                data={
                    "subcategory": {
                        "id": subcategory.id,
                        "name": subcategory.name
                    },
                    "total_documents": sub_btn.count(),
                    "documents": serializer.data
                }
            )

        except Object.DoesNotExist:
            return ErrorResponse(message="Object does not exist", status_code=404)

project_document_api_view = ProjectDocumentAPIView.as_view()



class NextStageDocumentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        projects = NextStageDocuments.objects.filter(project_document_id=pk)
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(projects, request)
        serializer = NextStageDocumentsSerializer(paginated_queryset, many=True)

        return ListResponse(
            data={"total": projects.count(), "documents": serializer.data},
        )

    def post(self, request):
        serializer = document_serializer.NextStageDocumentsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return PostResponse(
                data=serializer.data,
                message="Kerakli papkalar yaratildi"
            )

        return ErrorResponse(message="Yaratishda xatolik yuz berdi", errors=serializer.errors)

    def patch(self, request, pk=None):
        try:
            document = NextStageDocuments.objects.get(pk=pk)
        except NextStageDocuments.DoesNotExist:
            return ErrorResponse(message="Bu ID da dokument topilmadi", status_code=404)

        new_name = request.data.get('name')
        if not new_name:
            return ErrorResponse(message="Name maydonini kiritish shart", status_code=400)

        document.name = new_name
        document.save()
        return PutResponse(data={"name": document.name}, message="Nomi muvaffaqiyatli yangilandi")

next_stage_document_api_view = NextStageDocumentsAPIView.as_view()



class ProjectSectionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """Bo'limlarni olish"""
        try:
            sections = ProjectSections.objects.filter(next_stage_documents_id=pk)
            if not sections.exists():
                return ErrorResponse(message="Bo'limlar topilmadi.", status_code=404)

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(sections, request)
            serializer = document_serializer.ProjectSectionsSerializer(paginated_queryset, many=True)

            return ListResponse(
                data={"total": sections.count(), "sections": serializer.data},
                message="Barcha bo'limlar muvaffaqiyatli olindi"
            )
        except Exception as e:
            return ErrorResponse(message=str(e))

    def post(self, request):
        """Yangi bo'lim yaratish"""
        serializer = document_serializer.CreateProjectSectionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return PostResponse(
                data=serializer.data,
                message="Bo'lim muvaffaqiyatli yaratildi"
            )

        return ErrorResponse(message="Xatolik yuz berdi.", errors=serializer.errors)

    def patch(self, request, pk=None):
        """Bo'lim nomini o'zgartirish"""
        try:
            section = ProjectSections.objects.get(id=pk)
        except ProjectSections.DoesNotExist:
            return ErrorResponse(message="Bo'lim topilmadi.", status_code=404)

        new_name = request.data.get('name')
        if not new_name:
            return ErrorResponse(message="Name maydonini kiritish shart", status_code=400)

        section.name = new_name
        section.save()
        return PutResponse(data={"name": section.name}, message="Nomi muvaffaqiyatli yangilandi")

project_section_api_view = ProjectSectionsAPIView.as_view()



class MultipleFileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = document_serializer.MultipleFileUploadSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            uploaded_files = serializer.save()  
            response_serializer = document_serializer.FilesSerializer(uploaded_files, many=True)  
            return PostResponse(
                data=response_serializer.data,
                message="Fayllar muvaffaqiyatli yuklandi"
            )
        return ErrorResponse(errors=serializer.errors)

multiple_file_upload_api_view = MultipleFileUploadView.as_view()



class GetFilesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk=None):
        try:
            files = Files.objects.filter(document_id=pk)
            if not files.exists():
                return ErrorResponse(message="Tegishli fayllar topilmadi", status_code=status.HTTP_404_NOT_FOUND)
            
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(files, request)
            serializer = document_serializer.GetFilesSerializer(paginated_queryset, many=True)
            
            return ListResponse(data=serializer.data, message="Barcha fayllar")

        except Exception as e:
            return ErrorResponse(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

get_files_api_view = GetFilesAPIView.as_view()



class GetFilesSectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk=None):
        try:
            files = Files.objects.filter(project_section_id=pk)
            if not files.exists():
                return ErrorResponse(message="Tegishli fayllar topilmadi", status_code=status.HTTP_404_NOT_FOUND)

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(files, request)
            serializer = document_serializer.GetFilesSerializer(paginated_queryset, many=True)

            return ListResponse(data=serializer.data, message="Barcha fayllar")

        except Exception as e:
            return ErrorResponse(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

get_files_section_api_view = GetFilesSectionAPIView.as_view()



class FilesSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        document_id = request.query_params.get('document_id')
        project_section_id = request.query_params.get('project_section_id')
        search_query = request.query_params.get('query')

        if not search_query:
            return ErrorResponse(message="Qidiruv so'rovi (query) parametri talab qilinadi.", 
                                 status_code=status.HTTP_400_BAD_REQUEST)

        if document_id:
            files = Files.objects.filter(
                Q(document_id=document_id) & (
                    Q(name__icontains=search_query) |
                    Q(calendar__icontains=search_query) |
                    Q(file_code__icontains=search_query)
                )
            )
        elif project_section_id:
            files = Files.objects.filter(
                Q(project_section_id=project_section_id) & (
                    Q(name__icontains=search_query) |
                    Q(calendar__icontains=search_query) |
                    Q(file_code__icontains=search_query)
                )
            )
        else:
            return ErrorResponse(message="Document_id yoki project_section_idni kiritishingiz kerak.", 
                                 status_code=status.HTTP_400_BAD_REQUEST)

        if not files.exists():
            return ErrorResponse(message="Mos keluvchi fayllar topilmadi.", 
                                 status_code=status.HTTP_404_NOT_FOUND)

        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(files, request)
        result = paginated_queryset.values('name', 'files', 'file_code', 'calendar', 'created_at')
        return ListResponse(data=list(result), message="Qidiruv natijalari")

file_search_api_view = FilesSearchAPIView.as_view()



class NestedDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_params = request.query_params.get("query")

        if query_params not in ['1', '2', '3']:
            return ErrorResponse(message="Noto'g'ri query parametri kiritildi.", status_code=status.HTTP_400_BAD_REQUEST)

        try:
            paginator = CustomPagination()

            if query_params == '1':
                project_docs = ObjectsPassword.objects.filter(project_documentation__is_obj_password=True)
                paginated_queryset = paginator.paginate_queryset(project_docs, request)
                serializer = GetObjectsPasswordSerializer(paginated_queryset, many=True)
                return ListResponse(data=serializer.data, message="Hujjatlar ro'yxati")

            elif query_params == '2':
                sub_btns = Object.objects.prefetch_related(
                    Prefetch(
                        'nextstagedocuments_set',
                        queryset=NextStageDocuments.objects.filter(project_document__is_project_doc=True),
                        to_attr='filtered_docs'
                    )
                )
                data = [
                    {
                        "sub_btn_id": sub_btn.id,
                        "sub_btn_title": sub_btn.name,
                        "project_docs": NextStageDocumentsSerializer(
                            paginator.paginate_queryset(sub_btn.filtered_docs, request), many=True
                        ).data
                    }
                    for sub_btn in sub_btns
                ]
                return ListResponse(data=data, message="Barcha loyihalar")

            elif query_params == '3':
                project_docs = NextStageDocuments.objects.filter(project_document__is_work_smr=True)
                paginated_queryset = paginator.paginate_queryset(project_docs, request)
                serializer = NextStageDocumentsSerializer(paginated_queryset, many=True)
                return ListResponse(data=serializer.data, message="Ishchi SMR hujjatlari")

        except Exception as e:
            return ErrorResponse(message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

nested_data_api_view = NestedDataAPIView.as_view()



class ObjectsPasswordDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if not pk:
            return ErrorResponse(message="subcategory_btn_id talab qilinadi.", status_code=status.HTTP_400_BAD_REQUEST)

        get_password = ObjectsPassword.objects.filter(subcategory_btn_id=pk)
        if not get_password.exists():
            return ErrorResponse(message="Ma'lumot topilmadi.", status_code=status.HTTP_404_NOT_FOUND)
        
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(get_password, request)
        serializer = GetObjectsPasswordSerializer(paginated_queryset, many=True)
        return ListResponse(data=serializer.data, message="Obyekt pasporti ma'lumotlari")
    
object_password_detail_api_view = ObjectsPasswordDetailAPIView.as_view()



class StatisticalData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_statistics = ObjectCategory.objects.only("id", "name")
        if not all_statistics.exists():
            return ErrorResponse(message="Statistik ma'lumotlar topilmadi.", status_code=status.HTTP_404_NOT_FOUND)

        serializer = ObjectCategoryStatisticsSerializer(all_statistics, many=True)
        
        formatted_data = {
            item['name'].lower().replace(" ", "_"): item
            for item in serializer.data
        }
        return ListResponse(data=formatted_data, message="Statistik ma'lumotlar")

statistical_data_api_view = StatisticalData.as_view()








