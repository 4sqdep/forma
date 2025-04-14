from rest_framework import serializers
from main.apps.account.models.user import User
from main.apps.account.serializers.user import UserAllSerializer
from main.apps.employee_communication.models import EmployeeCommunication, FileMessage, TextMessage
from main.apps.object_passport.models.object import Object
from django.db.models import Count
from main.apps.object_passport.models.object import Object
from collections import OrderedDict


class ObjectTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
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



class TextMessageCreateSerializer(serializers.ModelSerializer):
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
            'sender',
            'is_read',
            'read_time'
        )



class TextMessageSerializer(serializers.ModelSerializer):
    # read_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    sender = UserAllSerializer()
    class Meta:
        model = TextMessage
        fields = (
            'employee_communication',
            'sender',
            # 'receiver',
            'text',
            # 'is_read',
            # 'read_time',
            'created_at'
        )

class FilterEmployeeCommunicationSerialize(serializers.ModelSerializer):
    class Meta:
        model = EmployeeCommunication
        fields = ['id', 'title']


class ObjectWithCommunicationsSerializer(serializers.ModelSerializer):
    communications = serializers.SerializerMethodField()
    counts = serializers.SerializerMethodField()

    class Meta:
        model = Object
        fields = ['id', 'title', 'communications', 'counts']

    def get_communications(self, obj):
        comms = EmployeeCommunication.objects.filter(obj=obj)
        return FilterEmployeeCommunicationSerialize(comms, many=True).data

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
