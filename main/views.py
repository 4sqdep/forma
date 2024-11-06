from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from account.permissions import check_user_permissions
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response({"message": 'success', 'data': serializer.data}, status=status.HTTP_200_OK)