from main.apps.account.models.user import User
from main.apps.account.serializers.user import (
    LoginSerializer, 
    Registerserializer, 
    UserProfileSerializer, 
    UserAllSerializer
)
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from main.apps.common.pagination import CustomPagination
from rest_framework import generics
from rest_framework.response import Response


class RegisterUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = Registerserializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Ma'lumot noto‘g‘ri kiritildi...", "errors": serializer.errors}
            )

        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data={"message": "Foydalanuvchi muvaffaqiyatli ro‘yxatdan o‘tkazildi!", "username": user.username}
        )

user_register_api_view = RegisterUser.as_view()



class LoginUser(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            token_data = response.data  

            return Response(
                status=status.HTTP_200_OK,
                data={"message": "Login successful", "token_data": token_data}
            )
        except (InvalidToken, TokenError) as e:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"message": "Invalid credentials", "errors": str(e)}
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "An unexpected error occurred", "errors": str(e)}
            )

user_login_api_view = LoginUser.as_view()



class UserProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk=None):
        try:
            userprofile = User.objects.get(id=pk)
            serializer = UserProfileSerializer(userprofile)
            return Response(
                status=status.HTTP_200_OK,
                data={"message": "Foydalanuvchi profili...", "data": serializer.data}
            )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "Foydalanuvchi topilmadi..."}
            )

    def post(self, request, pk=None):
        try:
            profile = User.objects.get(id=pk)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={"message": "Profil to'ldirildi!", "data": serializer.data}
                )
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Ma'lumot noto‘g‘ri kiritildi...", "errors": serializer.errors}
            )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "Foydalanuvchi topilmadi..."}
            )

    def put(self, request, pk=None):
        try:
            profile = User.objects.get(id=pk)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    status=status.HTTP_200_OK,
                    data={"message": "Profil yangilandi!", "data": serializer.data}
                )
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Ma'lumot noto‘g‘ri kiritildi...", "errors": serializer.errors}
            )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "Foydalanuvchi topilmadi..."}
            )

user_profile_api_view = UserProfileAPIView.as_view()



class AllUsersListAPIView(generics.ListAPIView):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserAllSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

all_user_api_view = AllUsersListAPIView.as_view()
