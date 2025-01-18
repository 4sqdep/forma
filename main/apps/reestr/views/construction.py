from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.reestr.models.construction import ConstructionTask
from ..serializers import construction as construction_task_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response




class ConstructionTaskCreateAPIView(generics.CreateAPIView):
    queryset = ConstructionTask.objects.all()
    serializer_class = construction_task_serializer.ConstructionTaskSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

construction_task_create_api_view = ConstructionTaskCreateAPIView.as_view()



class ConstructionTaskListAPIView(generics.ListAPIView):
    serializer_class = construction_task_serializer.ConstructionTaskSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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
        queryset = ConstructionTask.objects.all()
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
            response_data = Response(status=status.HTTP_200_OK, data=serializer.data)
        return response_data

construction_task_list_api_view = ConstructionTaskListAPIView.as_view()




class ConstructionTaskDetailAPIView(generics.RetrieveAPIView):
    queryset = ConstructionTask.objects.all()
    serializer_class = construction_task_serializer.ConstructionTaskSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            status = status.HTTP_200_OK,
            data=serializer.data
        )

construction_task_detail_api_view = ConstructionTaskDetailAPIView.as_view()




class ConstructionTaskUpdateAPIView(generics.UpdateAPIView):
    queryset = ConstructionTask.objects.all()
    serializer_class = construction_task_serializer.ConstructionTaskSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=serializer.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Successfully Updated'},
                status = status.HTTP_200_OK,
                data=serializer.data
                )
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

construction_task_update_api_view = ConstructionTaskUpdateAPIView.as_view()
    


class ConstructionTaskDeleteAPIView(generics.DestroyAPIView):
    queryset = ConstructionTask.objects.all()
    serializer_class = construction_task_serializer.ConstructionTaskSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Successfully deleted!'},
            status=status.HTTP_204_NO_CONTENT
        )

construction_task_delete_api_view = ConstructionTaskDeleteAPIView.as_view()