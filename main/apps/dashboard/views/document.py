from main.apps.dashboard.models.dashboard import DashboardSubCategoryButton
from main.apps.dashboard.models.document import Files, NextStageDocuments, ProjectSections, ProjectDocumentation
from main.apps.dashboard.serializers import document as document_serializer
from main.apps.dashboard.utils_serializers import NextStageDocumentsSerializer, ProjectDocumentationSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db.models import Case, When, Value, BooleanField
from main.apps.common.pagination import CustomPagination
from main.apps.dashboard.serializers.document import ProjectDocumentationSerializerHas


class ProjectDocumentAPIView(APIView):
    """Subkategoriya buttonga tegishli lo'yiha bo'limlarin olish"""
    permissions_classes = [IsAuthenticated]
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
        subcategory = DashboardSubCategoryButton.objects.get(id=pk)
        sub_btn = subcategory.projectdocumentation.all().order_by(order_case).annotate(
                has_data=Case(
                    When(name__isnull=False, then=Value(True)),  # Agar 'name' maydoni mavjud bo'lsa
                    default=Value(False),
                    output_field=BooleanField()
                )
            )
        serializer = ProjectDocumentationSerializerHas(sub_btn, many=True)
        return Response({'message': "Lo'yiha bo'limlari...", 'data': serializer.data}, status=status.HTTP_200_OK)


class NextStageDocumentsAPIView(APIView):
    """ProjectDocument ga tegishli loyiha asosiy bo'limlarini olish uchun"""
    permissions_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        projects = NextStageDocuments.objects.filter(project_document_id=pk)
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(projects, request)
        serializer = NextStageDocumentsSerializer(paginated_queryset, many=True)
        return Response({'message': "SuccessFull....", 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = document_serializer.NextStageDocumentsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
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


class ProjectSectionsAPIView(APIView):
    """Qo'shimcha bo'limlar yaratish uchun APIView"""
    permissions_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        """Bo'limlarni olish"""
        try:
            sections = ProjectSections.objects.filter(next_stage_documents_id=pk)
            if not sections.exists():
                return Response({"message": "Bo'limlar topilmadi."}, status=status.HTTP_404_NOT_FOUND)
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(sections, request)
            serializer = document_serializer.ProjectSectionsSerializer(paginated_queryset, many=True)
            return Response({"message": "Barcha bo'limlar.......", 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Yangi bo'lim yaratish"""
        serializer = document_serializer.CreateProjectSectionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Bo'lim muvaffaqiyatli yaratildi.", 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response({"message": "Xatolik yuz berdi.", 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk=None):
        """Bo'lim nomini o'zgartirish"""
        try:
            sections = ProjectSections.objects.get(id=pk)
        except ProjectSections.DoesNotExist:
            return Response({"message": "Bo'limlar topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        new_name = request.data.get('name')
        if not new_name:
            return Response({'nessage': "Name maydonini kiritilishi shart"}, status=status.HTTP_400_BAD_REQUEST)
        sections.name = new_name
        sections.save()
        return Response({"message": "Name muvaffaqiyatli yangilandi", 'data': sections.name}, status=status.HTTP_200_OK)


class MultipleFileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        serializer = document_serializer.MultipleFileUploadSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            uploaded_files = serializer.save()  # Fayllarni saqlash
            response_serializer = document_serializer.FilesSerializer(uploaded_files, many=True)  # Javobni formatlash
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
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(files, request)
            serializer = document_serializer.GetFilesSerializer(paginated_queryset, many=True)
            return Response({'message': "Barcha fayllar", 'data': serializer.data}, status=status.HTTP_200_OK)
        except Files.DoesNotExist as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


class GetFilesSectionAPIView(APIView):
    permissions_classes = [IsAuthenticated]
    multipart_parser_classes = [MultiPartParser, FormParser]
    def get(self, request, pk=None):
        try:
            files = Files.objects.filter(project_section_id=pk)
            if not files.exists():
                return Response({'message': "Tegishli fayllar topilmadi"}, status=status.HTTP_404_NOT_FOUND)
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(files, request)
            serializer = document_serializer.GetFilesSerializer(paginated_queryset, many=True)
            return Response({'message': "Barcha fayllar", 'data': serializer.data}, status=status.HTTP_200_OK)
        except Files.DoesNotExist as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


class FilesSearchAPIView(APIView):
    """
    `Files` modelidan `name`, `calendar`, va `file_code` maydonlarini qidirish.
    Prioritet: document_id > project_section_id.
    """

    def get(self, request, *args, **kwargs):
        document_id = request.query_params.get('document_id')  # ?document_id=1
        project_section_id = request.query_params.get('project_section_id')  # ?project_section_id=2
        search_query = request.query_params.get('query')  # Qidiruv so'zi (?q=example)

        if not search_query:
            return Response({"error": "Qidiruv so'rovi (query) parametri talab qilinadi."},
                status=status.HTTP_400_BAD_REQUEST)

        # Filtrlashni tashkil qilish
        if document_id:
            files = Files.objects.filter(Q(document_id=document_id) & (Q(name__icontains=search_query) |
                 Q(calendar__icontains=search_query) | Q(file_code__icontains=search_query)))
        elif project_section_id:
            files = Files.objects.filter(Q(project_section_id=project_section_id) & (Q(name__icontains=search_query) |
                 Q(calendar__icontains=search_query) | Q(file_code__icontains=search_query)))
        else:
            return Response({"error": "Document_id yoki project_section_idni kiritishingiz kerak."},
                status=status.HTTP_400_BAD_REQUEST)
        # Ma'lumotlar mavjudligini tekshirish
        if not files.exists():
            return Response({"message": "No matching files found."}, status=status.HTTP_404_NOT_FOUND)

        # Faqat kerakli maydonlarni qaytarish
        result = files.values('name', 'files', 'file_code', 'calendar', 'created_at')
        return Response(result, status=status.HTTP_200_OK)