from main.apps.account.models import ActivationSMSCode
from main.apps.account.utils import generate_random_otp, send_otp_to_telegram_group
from main.apps.common.pagination import CustomPagination
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from . import serializer  as user_serializer
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from ..account.send_otp import (
    send_otp,
    resetting_otp
    )
from django.contrib.auth.hashers import make_password
from datetime import datetime
from rest_framework_simplejwt import authentication
from main.apps.common.response import (
    DestroyResponse, 
    ListResponse, 
    PostResponse, 
    PutResponse
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


User = get_user_model()



class AuthUserRegistrationView(generics.CreateAPIView):
    serializer_class = user_serializer.UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return PostResponse(
                data=serializer.data,
                message="User",
                status_code=status.HTTP_201_CREATED,
                status=status.HTTP_201_CREATED
            )

user_registration_api_view = AuthUserRegistrationView.as_view()



class UserLoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = user_serializer.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            token_data = response.data 

            return PostResponse(
                data=token_data,
                status_code=status.HTTP_200_OK,
                message="Login Success",
                add_suffix=False
            )
        except (InvalidToken, TokenError) as e:
            return ListResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                data={'error': str(e), 'success': False}
            )
        except Exception as e:
            return ListResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                data={'error': str(e), 'success': False}
            )

user_login_api_view = UserLoginView().as_view()


# class OTPSendAPIView(generics.GenericAPIView):
#     serializer_class = user_serializer.ActivationCodeSerializer
#     queryset = ActivationSMSCode.objects.all()
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         valid = serializer.is_valid(raise_exception=True)
#         otp = generate_random_otp()
#         phone_number = serializer.validated_data["phone_number"]

#         if User.objects.filter(phone_number=phone_number).exists():
#             return ListResponse(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 data={"error": "This phone number is already associated with an existing user."},
#                 success=False
#             )
#         ActivationSMSCode.objects.create(
#             otp=otp,
#             phone_number=phone_number
#         )

#         phone_number = serializer.data["phone_number"]
#         chat_id = "-4592340981"  
#         bot_token = "7446593811:AAE5TCQTGjAznTW2lfI9BNDbB9S_nPLNoRc"
#         # otp = serializer.data["otp"]
#         # if User.objects.filter(phone_number=phone_number).exists(): 
#         #     return ListResponse(
#         #         status_code=status.HTTP_400_BAD_REQUEST,
#         #         data="This phone number already exists in the database",
#         #         # data={"user": serializer.data}
#         #     )
        
#         send_otp_to_telegram_group(otp, phone_number, chat_id, bot_token)
#         return PostResponse(
#             status_code=status.HTTP_201_CREATED,
#             message="OTP sent successfully!",
#             data={"user": serializer.data},
#             add_suffix=False
#         )

# otp_sent_api_view = OTPSendAPIView.as_view()


class VerifyPhoneOTP(generics.GenericAPIView):
    serializer_class = user_serializer.VerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.data['phone_number']
            otp = serializer.data['otp']
            activation_code = ActivationSMSCode.objects.filter(
                phone_number=phone_number
            ).first()
            
            if activation_code.otp != otp:
                return ListResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    data={'error': 'Wrong OTP, Something went wrong'}
                )
            
            dates = str(datetime.now().strftime('%H:%M:%S'))
            users_date = str(activation_code.otp_sent_time)
            
            if users_date < dates:
                return PostResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="OTP code expired, send again!",
                    data={'error': 'OTP expired'},
                    add_suffix=False
                )
            else:
                activation_code.is_verified = True
                activation_code.save()

                return PostResponse(
                    status_code=status.HTTP_200_OK,
                    message="Phone number is verified",
                    data={'phone_number': phone_number},
                    add_suffix=False
                )
        else:
            return ListResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Account does not exist!",
                data=serializer.errors
            )

user_otp_verify_api_view = VerifyPhoneOTP.as_view()



class ResendOtpToPhoneNumberAPIView(generics.GenericAPIView):
    serializer_class = user_serializer.UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        phone_number = data['phone_number']
        otp = generate_random_otp()

        chat_id = "-4592340981"  
        bot_token = "7446593811:AAE5TCQTGjAznTW2lfI9BNDbB9S_nPLNoRc"
        try:
            ActivationSMSCode.objects.create(
                otp=otp,
                phone_number=phone_number
            )
            user = User.objects.get(phone_number=phone_number)
            # send_otp(phone_number)
            send_otp_to_telegram_group(otp, phone_number, chat_id, bot_token)
            return PostResponse(
                status_code=status.HTTP_200_OK,
                message="OTP resent successfully",
                data={'phone_number': phone_number},
                add_suffix=False
            )
        except User.DoesNotExist:
            return ListResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User does not exist",
                data={'error': "No user found with this phone number"}
            )

user_resend_otp_api_view = ResendOtpToPhoneNumberAPIView.as_view()



class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = user_serializer.ActivationCodeSerializer
    queryset = ActivationSMSCode.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        otp = generate_random_otp()
        phone_number = serializer.validated_data["phone_number"]

        ActivationSMSCode.objects.create(
            otp=otp,
            phone_number=phone_number
        )

        phone_number = serializer.data["phone_number"]
        chat_id = "-4592340981"  
        bot_token = "7446593811:AAE5TCQTGjAznTW2lfI9BNDbB9S_nPLNoRc"
        # otp = serializer.data["otp"]
        # if User.objects.filter(phone_number=phone_number).exists(): 
        #     return ListResponse(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         data="This phone number already exists in the database",
        #         # data={"user": serializer.data}
        #     )
        
        send_otp_to_telegram_group(otp, phone_number, chat_id, bot_token)
        return PostResponse(
            status_code=status.HTTP_201_CREATED,
            message="OTP sent successfully!",
            data={"user": serializer.data},
            add_suffix=False
        )
    
    # serializer_class = user_serializer.PasswordResetSerializer
    # permission_classes = (permissions.AllowAny,)

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     valid = serializer.is_valid(raise_exception=True)
    #     data = request.data
    #     phone_number = data['phone_number']
    #     if valid:
    #         serializer.save()
    #         try:
    #             user = User.objects.get(phone_number=phone_number)
    #             # resetting_otp(phone_number)
    #             status_code = status.HTTP_201_CREATED
    #             return PostResponse(
    #                 status_code=status.HTTP_201_CREATED,
    #                 message="Code successfully sent",
    #                 data={'user': serializer.data},
    #                 add_suffix=False
    #             )
    #         except User.DoesNotExist:
    #             return ListResponse(
    #                 status_code=status.HTTP_400_BAD_REQUEST,
    #                 message="User does not exist",
    #                 data={'error': "No user found with this phone number"}
    #             )

password_reset_api_view = PasswordResetAPIView.as_view()


# class PasswordResetCodeCheckView(generics.GenericAPIView):
#     serializer_class = user_serializer.PasswordResetCodeCheckSerializer
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, *args, **kwargs):
#         dates = str(datetime.now().strftime('%H:%M:%S'))
#         serializer = self.get_serializer(data=request.data)                                                     
#         valid = serializer.is_valid(raise_exception=False)
#         if valid:
#             try:
#                 user = User.objects.get(activating_code=serializer.data['confirm_code'])
#                 # Uncomment if you need to check expiration time of the OTP
#                 # if user.user_sms.otp_sent_time_reset < dates:
#                 #     return ListResponse(
#                 #         status_code=status.HTTP_400_BAD_REQUEST,
#                 #         message="Code vaqti tugagan, qayta code jo'nating!",
#                 #         data={}
#                 #     )
#                 return PostResponse(
#                     status_code=status.HTTP_200_OK,
#                     message="Code tastiqlandi!", 
#                     data={'user': user.id},
#                     add_suffix=False  
#                 )
#             except User.DoesNotExist:
#                 return ListResponse(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     message="Sizga xozir jo'natilgan code ni kiriting!",
#                     data={}
#                 )
#         return ListResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             message="Serializer not valid!",
#             data={}
#         )

# password_reset_check_view = PasswordResetCodeCheckView.as_view()


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = user_serializer.PasswordResetConfirmSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = request.data 
        phone_number = data['phone_number']

        if serializer.is_valid(raise_exception=False):
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return ListResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="User does not exist",
                    data={}
                )
            if serializer.data['new_password1'] != serializer.data['new_password2']:
                return ListResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Two fields should be the same!",
                    data={}
                )
            else:
                user.password = make_password(serializer.data['new_password1'])
                user.save()
                return PostResponse(
                    status_code=status.HTTP_200_OK,
                    message="Password successfully updated",
                    data={'user': user.id},
                    add_suffix=False
                )
        else:
            return ListResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="The entered password is incorrect",
                data=serializer.errors
            )

password_reset_confirm_view = PasswordResetConfirmView.as_view()



class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = user_serializer.UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    partial = True  

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ListResponse(
            status_code=status.HTTP_200_OK, 
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return PutResponse(
                status_code=status.HTTP_200_OK, 
                message=f"Updated: {updated_instance.id}", 
                data=serializer.data
            )
        return ListResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            data=serializer.errors
        )

user_retrieve_update_api_view = UserRetrieveUpdateAPIView.as_view()



class UserListAPIView(generics.ListAPIView):
    serializer_class = user_serializer.UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    pagination_class = CustomPagination
    search_fields = ["phone_number",]  

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = User.objects.exclude(is_moderator=True).exclude(is_superuser=True)
        return queryset

    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.get_pagination_class()

        if paginator:
            paginator = paginator()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", None)
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data = ListResponse(status_code=status.HTTP_200_OK, data=serializer.data)
        return response_data

user_list_view = UserListAPIView.as_view()