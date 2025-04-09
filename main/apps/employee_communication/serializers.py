from rest_framework import serializers
from main.apps.employee_communication.models import EmployeeCommunication, FileMessage, TextMessage




class EmployeeCommunicationSerializer(serializers.ModelSerializer):
    read_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    
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
            'obj',
            'is_read',
            'read_time',
            'view_count'
        )
        read_only_fields = (
            'is_read',
            'read_time',
            'view_count'
        )
    
    def create(self, validated_data):
        employees = validated_data.pop('employee', [])
        communication = EmployeeCommunication.objects.create(**validated_data)
        communication.employee.set(employees)
        return communication



class FileMessageSerializer(serializers.ModelSerializer):
    read_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = FileMessage
        fields = (
            'employee_communication',
            'sender',
            'receiver',
            'file',
            'is_read',
            'read_time'
        )
        read_only_fields = (
            'is_read',
            'read_time'
        )



class TextMessageSerializer(serializers.ModelSerializer):
    read_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = TextMessage
        fields = (
            'employee_communication',
            'sender',
            'receiver',
            'text',
            'is_read',
            'read_time'
        )
        read_only_fields = (
            'is_read',
            'read_time'
        )