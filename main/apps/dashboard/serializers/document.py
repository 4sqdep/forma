from main.apps.dashboard.models.document import Files, NextStageDocuments, ProjectDocumentation, ProjectSections
from main.apps.dashboard.serializers.dashboard import DashboardSubCategoryButtonSerializerName
from rest_framework import serializers



class ProjectDocumentationSerializerHas(serializers.ModelSerializer):
    subcategories_btn = DashboardSubCategoryButtonSerializerName()
    project_count = serializers.IntegerField(read_only=True)
    has_data = serializers.BooleanField(read_only=True)
    class Meta:
        model = ProjectDocumentation
        fields = (
            'id', 
            'user', 
            'subcategories_btn', 
            'name', 
            'project_count',
            'has_data', 
            'is_obj_password', 
            'is_project_doc', 
            'is_work_smr', 
            'is_equipment', 
            'created_at'
        )


class NextStageDocumentsSerializer(serializers.ModelSerializer):
    """Keyingi hujjatlar uchun serializer"""
    class Meta:
        model = NextStageDocuments
        fields = ['id', 'name', 'is_forma', 'is_section']


class NextStageDocumentsCreateSerializer(serializers.ModelSerializer):
    """Keyingi hujjatlar uchun papakalar yaratish uchun serializer"""
    class Meta:
        model = NextStageDocuments
        fields = ['id', 'project_document', 'subcategories_btn', 'name', 'is_forma', 'is_section']


class FilesSerializer(serializers.ModelSerializer):
    """Fayllarni yuklash uchun serializer"""
    class Meta:
        model = Files
        fields = '__all__'


class MultipleFileUploadSerializer(serializers.Serializer):
    document_id = serializers.IntegerField(required=False)  # NextStageDocuments modelining IDsi
    project_section_id = serializers.IntegerField(required=False)  # ProjectSections IDsi
    name = serializers.CharField(max_length=1000, required=False)  # Fayl nomi
    calendar = serializers.CharField(max_length=30, required=False)  # Hujjat sanasi
    file_code = serializers.CharField(max_length=30, required=False)
    files = serializers.ListField(child=serializers.FileField(), allow_empty=False, write_only=True)

    def validate(self, attrs):
        document_id = attrs.get('document_id')
        project_section_id = attrs.get('project_section_id')
        # Faqat bitta maydon to'ldirilganligini tekshirish
        if not document_id and not project_section_id:
            raise serializers.ValidationError("Document id yoki project_section idni kiritishingiz kerak.")
        if document_id and project_section_id:
            raise serializers.ValidationError("Siz faqat document_id yoki project_section_id dan birini taqdim etishingiz mumkin.")
        return attrs

    def create(self, validated_data):
        document_id = validated_data.get('document_id')
        project_section_id = validated_data.get('project_section_id')
        files = validated_data.get('files')
        name = validated_data.get('name')
        file_code = validated_data.get('file_code')
        calendar = validated_data.get('calendar')

        document = None
        project_section = None

        # `document` yoki `project_section`ni olish
        if document_id:
            try:
                document = NextStageDocuments.objects.get(id=document_id)
            except NextStageDocuments.DoesNotExist:
                raise serializers.ValidationError({"document_id": "NextStageDocuments topilmadi."})
        if project_section_id:
            try:
                project_section = ProjectSections.objects.get(id=project_section_id)
            except ProjectSections.DoesNotExist:
                raise serializers.ValidationError({"project_section_id": "ProjectSections topilmadi."})

        # Fayllar ro'yxatini yaratish
        file_instances = [
            Files(document=document, project_section=project_section, user=self.context['request'].user,  # Foydalanuvchini olish
                name=name, calendar=calendar, file_code=file_code, files=file)
            for file in files
        ]

        # Fayllarni bir vaqtda bazaga qo'shish
        Files.objects.bulk_create(file_instances)
        return file_instances


class GetFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['id', 'files', 'name', 'file_code', 'calendar', 'created_at']


class ProjectSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSections
        fields = ['id', 'name', 'created_at']


class CreateProjectSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSections
        fields = ['id', 'next_stage_documents', 'user', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
