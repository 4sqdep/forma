import re
from .models import ActivationSMSCode, User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import generate_random_password, send_password_to_telegram_group
from django.conf import settings


class UserRegistrationSerializer(serializers.ModelSerializer):   
    confirm_password = serializers.CharField(
        write_only = True,
        required = False,
        help_text = 'Enter confirm password',
        style = {'input_type': 'password'}
    )
    password = serializers.CharField(
        write_only=True,
        required=False,  
        help_text='Enter password',
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            'phone_number',
            "profile_picture",
            "date_of_birth",
            "passport_series",
            "position",
            'password',
            'confirm_password'
        )    

    def to_internal_value(self, data):
        data = data.copy()
        random_password = generate_random_password()
        print('random_password', random_password)

        phone_number = data.get('phone_number', 'Unknown')
        chat_id = "-4592340981"  
        bot_token = "7446593811:AAE5TCQTGjAznTW2lfI9BNDbB9S_nPLNoRc"  
        send_password_to_telegram_group(random_password, phone_number, chat_id, bot_token)

        data['password'] = random_password
        data['confirm_password'] = random_password
        return super().to_internal_value(data)
    

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        auth_user = User.objects.create_user(**validated_data)
        return auth_user


class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        data['id'] = self.user.id
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name

        if self.user.profile_picture:
            data['profile_picture'] = settings.MEDIA_URL + str(self.user.profile_picture)
            data['profile_picture'] = self.context['request'].build_absolute_uri(data['profile_picture'])
        else:
            data['profile_picture'] = None
        data['position'] = self.user.position
        return data
    


class UserDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "guid",
            "first_name",
            "last_name",
            "middle_name",
            "phone_number",
            "profile_picture",
            "date_of_birth",
            "passport_series",
            "position",
            "is_active",
            'created_at'
        )
    


class PasswordResetSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')

        if not phone_number.startswith('+998'):
            raise serializers.ValidationError(
                "Phone number must start with '+998'."
            )
        return attrs

    def create(self, validated_data):
        return validated_data


class PasswordResetCodeCheckSerializer(serializers.Serializer):
    confirm_code = serializers.CharField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()


class VerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()


class ActivationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivationSMSCode
        fields = ('phone_number',)