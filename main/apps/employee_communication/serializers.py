from rest_framework import serializers
from main.apps.account.models.user import User
from main.apps.account.serializers.user import UserAllSerializer
from main.apps.employee_communication.models import EmployeeCommunication, FileMessage, TextMessage
from main.apps.object_passport.models.object import Object
from django.db.models import Count
from main.apps.object_passport.models.object import Object
from collections import OrderedDict
from main.apps.object_passport.serializers.object import ObjectTitleSerializer




class BaseEmployeeCommunicationSerialize(serializers.ModelSerializer):
    class Meta:
        model = EmployeeCommunication
        fields = ['id', 'title']



class EmployeeCommunicationCreateSerializer(serializers.ModelSerializer):
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
    


class EmployeeCommunicationSerializer(serializers.ModelSerializer):
    employee = UserAllSerializer(many=True)
    obj = ObjectTitleSerializer()
    read_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    sender = UserAllSerializer()
    
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
