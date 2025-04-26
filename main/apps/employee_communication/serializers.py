from rest_framework import serializers
from main.apps.account.serializers.user import UserAllSerializer
from main.apps.employee_communication.models import (
    EmployeeCommunication, 
    EmployeeCommunicationRecipient, 
    FileMessage, 
    TextMessage
)
from main.apps.object_passport.models.object import Object
from django.db.models import Count
from collections import OrderedDict
from main.apps.object_passport.serializers.object import ObjectTitleSerializer




class BaseEmployeeCommunicationSerialize(serializers.ModelSerializer):
    class Meta:
        model = EmployeeCommunication
        fields = ['id', 'title']



class EmployeeCommunicationCreateSerializer(serializers.ModelSerializer):
    employee = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = EmployeeCommunication
        fields = (
            'title', 
            'comment', 
            'file', 
            'deadline', 
            'status',
            'section_type', 
            'obj', 
            'employee'
        )

    def create(self, validated_data):
        employee = validated_data.pop('employee', [])
        communication = EmployeeCommunication.objects.create(**validated_data)

        for emp_id in employee:
            EmployeeCommunicationRecipient.objects.create(
                communication=communication,
                employee_id=emp_id
            )
        return communication



class EmployeeCommunicationSerializer(serializers.ModelSerializer):
    recipients = serializers.SerializerMethodField()
    obj = ObjectTitleSerializer()
    sender = UserAllSerializer()
    is_read = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    file = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeCommunication 
        fields = (
            'id',
            'sender',
            'title',
            'comment',
            'file',
            'recipients',  
            'deadline',
            'status',
            'section_type',
            'obj',
            'is_read',
            'created_at'
        )

    def get_recipients(self, obj):
        recipient_qs = EmployeeCommunicationRecipient.objects.filter(communication=obj)
        return EmployeeCommunicationRecipientSerializer(recipient_qs, many=True).data
    
    def get_is_read(self, obj):
        return EmployeeCommunicationRecipient.objects.filter(
            communication=obj,
            is_read=True
        ).exists()
    
    def get_file(self, obj):
        from urllib.parse import unquote
        
        if obj.file:
            file_url = obj.file.url
            filename_encoded = file_url.split("/")[-1]
            filename = unquote(filename_encoded)
            return filename.replace(" ", "_")
        return None



class EmployeeCommunicationRecipientSerializer(serializers.ModelSerializer):
    read_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    employee = UserAllSerializer()

    class Meta:
        model = EmployeeCommunicationRecipient
        fields = ['employee', 'is_read', 'read_time', 'view_count']



class FileMessageCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)
    class Meta:
        model = FileMessage
        fields = (
            'employee_communication',
            'sender',
            'file'
        )


class FileMessageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    sender = UserAllSerializer()
    file_size = serializers.SerializerMethodField()
    class Meta:
        model = FileMessage
        fields = (
            'employee_communication',
            'sender',
            'file',
            'file_size',
            'created_at'
        )
    
    def get_file_size(self, obj):
        if obj.file and hasattr(obj.file, 'size'):
            size = obj.file.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 ** 2:
                return f"{size / 1024:.2f} KB"
            elif size < 1024 ** 3:
                return f"{size / (1024 ** 2):.2f} MB"
            else:
                return f"{size / (1024 ** 3):.2f} GB"
        return None

        


class TextMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMessage
        fields = (
            'employee_communication',
            'sender',
            'text',
        )
        


class TextMessageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    sender = UserAllSerializer()
    class Meta:
        model = TextMessage
        fields = (
            'employee_communication',
            'sender',
            'text',
            'created_at'
        )



class ObjectWithCommunicationsSerializer(serializers.ModelSerializer):
    communications = serializers.SerializerMethodField()
    counts = serializers.SerializerMethodField()

    class Meta:
        model = Object
        fields = ['id', 'title', 'communications', 'counts']

    def get_communications(self, obj):
        comms = EmployeeCommunication.objects.filter(obj=obj)
        return BaseEmployeeCommunicationSerialize(comms, many=True).data

    def get_counts(self, obj):
        # 1. Belgilangan tartibda statuslar
        status_order = [
            'new',
            'done',
            'in_confirmation',
            'in_progress',
            'incomplete',
            'completed_late'
        ]

        # 2. Umumiy muammo soni
        all_communications = EmployeeCommunication.objects.filter(obj=obj)
        total = all_communications.count()

        # 3. Guruhlab sanash
        raw_counts = (
            all_communications
            .values('status')
            .annotate(count=Count('status'))
        )
        counted = {item['status']: item['count'] for item in raw_counts}

        # 4. To‘liq tartibli dict hosil qilish
        ordered_counts = OrderedDict()
        ordered_counts['all'] = total
        for status in status_order:
            ordered_counts[status] = counted.get(status, 0)

        return ordered_counts
