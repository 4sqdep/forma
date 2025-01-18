from main.apps.account.models.user import User
from main.apps.account.serializers.user import LoginSerializer, Registerserializer, UserProfileSerializer, UserAllSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from main.apps.common.pagination import CustomPagination
from rest_framework import generics

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
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            token_data = response.data 

            return Response(
                data=token_data,
                status=status.HTTP_201_CREATED,
            )
        except (InvalidToken, TokenError) as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': str(e), 'success': False}
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': str(e), 'success': False}
            )

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
        try:
            profile = User.objects.get(id=pk)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': "Profile to'ldirildi!", 'data': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': "Foydalanuvchi topilmadi....."}, status=status.HTTP_404_NOT_FOUND)


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


class AllUsersListAPIView(generics.ListAPIView):
    """Barcha foydalanuvchilarni olish faqat is_superuser=False qiymatga ega bo'lganlarini"""
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserAllSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
