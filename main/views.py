from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from account.permissions import CanGetPermission
from .models import Post
from account.models import UserProfile
from .serializers import PostSerializer


class PostList(APIView):
    permission_classes = [CanGetPermission, IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response({"message": 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Malumot saqaland", 'data': serializer.data}, status=status.HTTP_201_CREATED)