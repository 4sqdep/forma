# from main.apps.dashboard.models.document import NextStageDocuments, ProjectDocumentation
# from rest_framework import serializers



# class NextStageDocumentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NextStageDocuments
#         fields = ['id', 'created_by', 'name', 'is_forma', 'is_section', 'is_file']


# class ProjectDocumentationSerializer(serializers.ModelSerializer):
#     documents = NextStageDocumentsSerializer(many=True, read_only=True)
#     class Meta:
#         model = ProjectDocumentation
#         fields = ['id', 'name', 'documents']