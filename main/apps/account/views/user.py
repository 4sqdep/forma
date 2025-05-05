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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from main.apps.role.permissions import IsSuperUser





class RegisterUser(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]

    def post(self, request):
        serializer = Registerserializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Ma'lumot noto‘g‘ri kiritildi...", "errors": serializer.errors}
            )

        user = serializer.save()
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
    serializer_class = UserAllSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]
    pagination_class = CustomPagination

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
        queryset = User.objects.filter(is_superuser=False)
        return queryset
    
    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator_class = self.get_pagination_class()

        if paginator_class:
            paginator = paginator_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", [])
            return response_data

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)

all_user_api_view = AllUsersListAPIView.as_view()
