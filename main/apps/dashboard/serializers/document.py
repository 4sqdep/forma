from main.apps.dashboard.models.document import DocumentFiles, NextStageDocuments, ProjectDocumentation, ProjectSections
from main.apps.dashboard.serializers.dashboard import ObjectSerializer
from rest_framework import serializers



class ProjectDocumentationSerializerHas(serializers.ModelSerializer):
    object = ObjectSerializer()
    project_count = serializers.IntegerField(read_only=True)
    has_data = serializers.BooleanField(read_only=True)
    first_name = serializers.CharField(source='created_by.first_name', read_only=True)
    last_name = serializers.CharField(source='created_by.last_name', read_only=True)
    class Meta:
        model = ProjectDocumentation
        fields = (
            'id',
            'first_name',
            'last_name',
            'object', 
            'name', 
            'project_count',
            'has_data', 
            'is_obj_password', 
            'is_project_doc', 
            'is_work_smr', 
            'is_equipment'
        )


class NextStageDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextStageDocuments
        fields = (
            'id', 
            'object',
            'name',
            'is_forma',
            'is_section',
            'is_file'
        )


class NextStageDocumentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextStageDocuments
        fields = (
            'id',
            'object',
            'name', 
            'is_forma',
            'is_section', 
            'is_file'
        )



class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFiles
        fields = '__all__'


class MultipleFileUploadSerializer(serializers.Serializer):
    document_id = serializers.IntegerField(required=False)  
    project_section_id = serializers.IntegerField(required=False) 
    name = serializers.CharField(max_length=1000, required=False)  
    calendar = serializers.CharField(max_length=30, required=False)  
    file_code = serializers.CharField(max_length=30, required=False)
    files = serializers.ListField(child=serializers.FileField(), allow_empty=False, write_only=True)

    def validate(self, attrs):
        document_id = attrs.get('document_id')
        project_section_id = attrs.get('project_section_id')
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

        file_instances = [
            DocumentFiles(document=document,
                    project_section=project_section,
                    created_by=self.context['request'].user,  
                    name=name, calendar=calendar,
                    file_code=file_code, files=file)
            for file in files
        ]

        DocumentFiles.objects.bulk_create(file_instances)
        return file_instances


class GetFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFiles
        fields = (
            'id', 
            'files', 
            'name', 
            'file_code', 
            'calendar'
        )


class ProjectSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSections
        fields = (
            'id', 
            'name'
        )


class CreateProjectSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSections
        fields = (
            'id', 
            'next_stage_documents', 
            'name'
        )



class NextStageDocumentsSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = NextStageDocuments
        fields = (
            'id',
            'name',
        )


class ProjectDocumentationSerializer(serializers.ModelSerializer):
    documents = NextStageDocumentsSerializer(many=True, read_only=True)
    class Meta:
        model = ProjectDocumentation
        fields = (
            'id', 
            'name', 
            'documents'
        )