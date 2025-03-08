from rest_framework import generics, status, permissions 
from rest_framework_simplejwt import authentication
from main.apps.common.pagination import CustomPagination
from main.apps.dashboard.models.construction_installation_work import ConstructionInstallationFile, ConstructionInstallationProject, ConstructionInstallationSection, ConstructionInstallationStatistics, ConstructionInstallationSubSection, MonthlyCompletedTask
from ..serializers import construction_installation_work as construction_installation_work_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q



class ConstructionInstallationSectionAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConstructionInstallationSection.objects.all()


class ConstructionInstallationSectionListCreateAPIView(ConstructionInstallationSectionAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationSectionSerializer


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by object title', type=openapi.TYPE_STRING),
        ]
    )
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title=search)

        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

construction_installation_section_list_create_api_view = ConstructionInstallationSectionListCreateAPIView.as_view()



class ConstructionInstallationSectionRetrieveUpdateDeleteAPIView(ConstructionInstallationSectionAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationSectionSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "ConstructionInstallationSection updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "ConstructionInstallationSection deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_section_detail_update_delete_api_view = ConstructionInstallationSectionRetrieveUpdateDeleteAPIView.as_view()



class ConstructionInstallationFileAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConstructionInstallationFile.objects.all()


class ConstructionInstallationFileListCreateAPIView(ConstructionInstallationFileAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationFileSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by object title', type=openapi.TYPE_STRING),
            openapi.Parameter('section', openapi.IN_QUERY, description='Filter by section ID', type=openapi.TYPE_INTEGER),
        ]
    )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        section = self.kwargs.get('section')
        search = request.query_params.get('search')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(file_code__icontains=search) | 
                Q(full_name__icontains=search)
            )

        if section:
            queryset = queryset.filter(section=section)

        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

construction_installation_file_list_create_api_view = ConstructionInstallationFileListCreateAPIView.as_view()



class ConstructionInstallationFileRetrieveUpdateDeleteAPIView(ConstructionInstallationFileAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationFileSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Construction Installation File updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Construction Installation File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_file_detail_update_delete_api_view = ConstructionInstallationFileRetrieveUpdateDeleteAPIView.as_view()



class ConstructionInstallationStatisticsAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConstructionInstallationStatistics.objects.all()


class ConstructionInstallationStatisticsListCreateAPIView(ConstructionInstallationStatisticsAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationStatisticsSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by contractor', type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        obj = self.kwargs.get('object')
        # section = request.query_params.get('section')
        # search = request.query_params.get('search')
        # date = request.query_params.get('date')

        # if search:
        #     queryset = queryset.filter(Q(contractor__icontains=search))

        # if section:
        #     queryset = queryset.filter(construction_installation_section=section)

        # if date:
        #     queryset = queryset.filter(date=date)

        if obj:
            queryset = queryset.filter(object=obj)

        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

construction_installation_statistics_list_create_api_view = ConstructionInstallationStatisticsListCreateAPIView.as_view()


class ConstructionInstallationStatisticsRetrieveUpdateDeleteAPIView(ConstructionInstallationStatisticsAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationStatisticsSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Construction Installation Statistics updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Construction Installation Statistics deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_statistics_detail_update_delete_api_view = ConstructionInstallationStatisticsRetrieveUpdateDeleteAPIView.as_view()



class ConstructionInstallationSubSectionAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConstructionInstallationSubSection.objects.all()


class ConstructionInstallationSubSectionListCreateAPIView(ConstructionInstallationSubSectionAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationSubSectionSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by title', type=openapi.TYPE_STRING),
            openapi.Parameter('section', openapi.IN_QUERY, description='Filter by section ID', type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

construction_installation_sub_section_list_create_api_view = ConstructionInstallationSubSectionListCreateAPIView.as_view()


class ConstructionInstallationSubSectionRetrieveUpdateDeleteAPIView(ConstructionInstallationSubSectionAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationSubSectionSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Construction Installation SubSection updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Construction Installation SubSection deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_sub_section_detail_update_delete_api_view = ConstructionInstallationSubSectionRetrieveUpdateDeleteAPIView.as_view()


# ===================== Construction Installation Project Views =====================

class ConstructionInstallationProjectAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ConstructionInstallationProject.objects.all()


class ConstructionInstallationProjectListCreateAPIView(ConstructionInstallationProjectAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationProjectSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by project title', type=openapi.TYPE_STRING),
            openapi.Parameter('section', openapi.IN_QUERY, description='Filter by section ID', type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
    
construction_installation_project_list_create_api_view = ConstructionInstallationProjectListCreateAPIView.as_view()


class ConstructionInstallationProjectRetrieveUpdateDeleteAPIView(ConstructionInstallationProjectAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.ConstructionInstallationProjectSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Construction Installation Project updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Construction Installation Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

construction_installation_project_detail_update_delete_api_view = ConstructionInstallationProjectRetrieveUpdateDeleteAPIView.as_view()


# ===================== Monthly Completed Task Views =====================

class MonthlyCompletedTaskAPIView:
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = MonthlyCompletedTask.objects.all()


class MonthlyCompletedTaskListCreateAPIView(MonthlyCompletedTaskAPIView, generics.ListCreateAPIView):
    serializer_class = construction_installation_work_serializer.MonthlyCompletedTaskSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p', openapi.IN_QUERY, description='Pagination Parameter', type=openapi.TYPE_STRING),
            openapi.Parameter('project', openapi.IN_QUERY, description='Filter by project ID', type=openapi.TYPE_INTEGER),
            openapi.Parameter('date', openapi.IN_QUERY, description='Filter by date (YYYY-MM-DD)', type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = CustomPagination() if request.query_params.get('p') else None
        if paginator:
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
            response.data["status_code"] = status.HTTP_200_OK
            response.data["data"] = response.data.pop("results", [])
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

monthly_completed_task_list_create_api_view = MonthlyCompletedTaskListCreateAPIView.as_view()


class MonthlyCompletedTaskRetrieveUpdateDeleteAPIView(MonthlyCompletedTaskAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = construction_installation_work_serializer.MonthlyCompletedTaskSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Monthly Completed Task updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Monthly Completed Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

monthly_completed_task_detail_update_delete_api_view = MonthlyCompletedTaskRetrieveUpdateDeleteAPIView.as_view()
