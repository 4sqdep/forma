from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .serializers import (
    SearchObjectsNameSerializer,
)
from ..dashboard.models.dashboard import Object
from rest_framework.response import Response
from rest_framework import status




class SearchObjectsNameAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        q = request.query_params.get('query')
        if not q:
            return Response(data={"message": "Qidiruv so'rovi (query) parametri talab qilinadi."}, status=status.HTTP_400_BAD_REQUEST)

        obj_name = Object.objects.filter(Q(name__icontains=q))
        serializer = SearchObjectsNameSerializer(obj_name, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK, headers={"message": "Siz izlagan ma'lumotlar"})

search_object_name_api_view = SearchObjectsNameAPIView.as_view()
