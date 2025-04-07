from rest_framework import serializers
from main.apps.employee_communication.models import EmployeeCommunication, FileMessage, TextMessage
from django.contrib.contenttypes.models import ContentType




class EmployeeCommunicationSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.filter(
            model__in=[
                'projectdocumenttype',
                'constructioninstallationsection',
                'hydrostation'
            ]
        ),
        slug_field='model'
    )
    object_id = serializers.IntegerField()
    
    class Meta:
        model = EmployeeCommunication 
        fields = (
            'id',
            'sender',
            'title',
            'comment',
            'file',
            'employee',
            'deadline',
            'status',
            'content_type',
            'object_id'
        )


    def validate(self, data):
        model_class = data['content_type'].model_class()
        try:
            model_class.objects.get(pk=data['object_id'])
        except model_class.DoesNotExist:
            raise serializers.ValidationError({"object_id": "Object with this ID does not exist."})
        return data 
    
    def create(self, validated_data):
        employee_data = validated_data.pop('employee', [])
        employee_communication = EmployeeCommunication.objects.create(**validated_data)
        if employee_data:
            employee_communication.employee.set(employee_data)
        return employee_communication



class FileMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMessage
        fields = (
            'employee_communication',
            'sender',
            'receiver',
            'file'
        )



class TextMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMessage
        fields = (
            'employee_communication',
            'sender',
            'receiver',
            'text'
        )