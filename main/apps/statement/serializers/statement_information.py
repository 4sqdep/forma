from main.apps.account.serializer import UserDetailSerializer
from main.apps.statement.models.statement_information import StatementInformation
from rest_framework import serializers 



class StatementInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementInformation
        fields = (
            'id',
            'statement',
            'discount_percent',
            'discount_sum',
            'duration_date',
            'statament_comment',
            'comment_for_employee'
        )


class StatementInformationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementInformation
        fields = (
            'id',
            'statement',
            'discount_percent',
            'discount_sum',
            'duration_date',
            'statament_comment',
            'comment_for_employee'
        )
    


class StatementInformationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementInformation
        fields = (
            'statement',
            'discount_percent',
            'discount_sum',
            'duration_date',
            'statament_comment',
            'comment_for_employee'
        )