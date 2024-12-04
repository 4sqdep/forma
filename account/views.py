from functools import partial

from django.views.static import serve
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import Registerserializer, LoginSerializer, UserProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class RegisterUser(APIView):
    """
    Foydalanuvchini tizimga kirish uchun ro'yxatdan o'tkazish uchun view
    fields = ['username', 'password']
    """
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = Registerserializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': "Malumot kiritilmadi...", 'data': serializer.data},
                            status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({'message': "Foydalanuvchi ro'yxatdan o'tkazildi...."},
                        status=status.HTTP_201_CREATED)


class LoginUser(TokenObtainPairView):
    """Foydalanuvchi tizimga kirish uchun view"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer


user_login_api_view = LoginUser.as_view()


class UserProfileAPIView(APIView):
    """Foydalanuvchi profilini to'ldirish va yangilash"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk=None):
        userprofile = User.objects.get(id=pk)
        serializer = UserProfileSerializer(userprofile)
        return Response({'message': "Foydalanuvchi profili....", 'data': serializer.data})

    def post(self, request, pk=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Profile to'ldirildi!", 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk=None):
        try:
            profile = User.objects.get(id=pk)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': "Profil yangilandi....", 'data': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': "Foydalanuvchi topilmadi"}, status=status.HTTP_400_BAD_REQUEST)