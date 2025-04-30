from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import permissions, status
from main.apps.common.pagination import CustomPagination
from rest_framework_simplejwt import authentication
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from main.apps.contract.models import ContractSection, ContractFile
from main.apps.contract.serializers import ContractSectionSerializer, ContractSectionFileSerializer
from rest_framework.views import APIView
from django.db.models import Q




class ContractSectionCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializer = ContractSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': "Contract Section successfully created",
                'status_code': status.HTTP_201_CREATED,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': "Error creating Contract Section",
            'status_code': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

create_contract_api_view = ContractSectionCreateAPIView.as_view()



class ContractSectionListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ContractSectionSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("object", openapi.IN_QUERY, description="Filter by object ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("title", openapi.IN_QUERY, description="Filter by title", type=openapi.TYPE_STRING),
        ]
    )
    def get_queryset(self):
        contract_section = self.kwargs.get("contract_section")
        queryset = ContractSection.objects.select_related('object').all().order_by('id')
        if contract_section:
            queryset = queryset.filter(object=contract_section)
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
            response_data.data['status_code'] = status.HTTP_200_OK
            response_data.data['data'] = response_data.data.pop("results", [])
            return Response({'data': response_data.data, 'status_code': status.HTTP_200_OK},
                            status=status.HTTP_200_OK)
        serializer = ContractSectionSerializer(queryset, many=True)
        return Response({
            'message': 'Contract Section List successfully',
            'status_code': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

list_contract_section_api_view = ContractSectionListAPIView.as_view()



class ContractSectionsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ContractSectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContractSection.objects.select_related("object").all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': "ContractSection tafsilotlari muvaffaqiyatli olindi",
            "status_code": status.HTTP_200_OK,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

detail_contract_section_api_view = ContractSectionsRetrieveAPIView.as_view()



class ContractSectionUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ContractSectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContractSection.objects.select_related("object").all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': "Contract Section muvaffaqiyatli yangilandi",
                'status_code': status.HTTP_204_NO_CONTENT,
                'data': serializer.data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "message": "Contract Section yangilashda xatolik yuzberdi....",
            'status_code': status.HTTP_400_BAD_REQUEST,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

update_contract_section_api_view = ContractSectionUpdateAPIView.as_view()



class ContractSectionDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContractSection.objects.select_related("object").all()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Contract Section successfully deleted",
                         "status_code": status.HTTP_204_NO_CONTENT
                         }, status=status.HTTP_204_NO_CONTENT)

delete_contract_section_api_view = ContractSectionDelete.as_view()



class ContractFileCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request):
        serializer = ContractSectionFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': "Contract File successfully created",
                'status_code': status.HTTP_201_CREATED,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': "Error creating Contract File",
            'status_code': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

create_contract_file_api_view = ContractFileCreateAPIView.as_view()



class ContractFileListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ContractSectionFileSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("section", openapi.IN_QUERY, description="Filter by File ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("title", openapi.IN_QUERY, description="Filter by title", type=openapi.TYPE_STRING),
            openapi.Parameter("file_code", openapi.IN_QUERY, description="Filter by file code", type=openapi.TYPE_STRING),
        ]
    )
    def get_queryset(self):
        contract_file = self.kwargs.get("contract_file")
        queryset = ContractFile.objects.select_related('section').all()
        if contract_file:
            queryset = queryset.filter(section=contract_file)
        return queryset
    def get_pagination_class(self):
        p = self.request.query_params.get('p')
        if p:
            return CustomPagination
        return None
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator_class = self.get_pagination_class()

        if paginator_class:
            paginator = paginator_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data["status_code"] = status.HTTP_200_OK
            response_data.data["data"] = response_data.data.pop("results", [])
            return Response(response_data.data, status=status.HTTP_200_OK)

        serializer = ContractSectionFileSerializer(queryset, many=True)
        return Response({
            'message': "Contract File List successfully",
            'status_code': status.HTTP_200_OK,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

list_contract_file_api_view = ContractFileListAPIView.as_view()



class ContractFileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ContractSectionFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ContractFile.objects.select_related("section").all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': "Contract File muvaffaqiyatli yangilandi",
                'status_code': status.HTTP_204_NO_CONTENT,
                'data': serializer.data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "message": "Contract File yangilashda xatolik yuzberdi....",
            'status_code': status.HTTP_400_BAD_REQUEST,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

update_contract_file_api_view = ContractFileUpdateAPIView.as_view()



class ContractFilesDelete(generics.DestroyAPIView):
    serializer_class = ContractSectionFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContractFile.objects.select_related("section").all()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "File successfully deleted", "status_code": status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)

delete_contract_file_api_view = ContractFilesDelete.as_view()



class SearchContractAPIView(APIView):
    def get(self, request):
        queryset = ContractFile.objects.all()
        search_query = request.query_params.get('file', None)
        section_id = request.query_params.get('3', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(date__contains=search_query) |
                Q(file_code__contains=search_query)
            )

        if section_id:
            queryset = queryset.filter(section_id=section_id)
        serializer = ContractSectionFileSerializer(queryset, many=True)
        return Response({'message': "Siz izlagan malumot", 'data': serializer.data}, status=status.HTTP_200_OK)

search_contract_section_api_view = SearchContractAPIView.as_view()

