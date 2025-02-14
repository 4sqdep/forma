from main.apps.dashboard.models.dashboard import (
    ObjectCategory, 
    ObjectSubCategory, 
    Object
)
from main.apps.dashboard.serializers.dashboard import (
    ObjectCategorySerializer, 
    ObjectSubCategorySerializer, 
    ObjectSerializer
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Case, When, Value, BooleanField
from ...common.response import (
    ListResponse,
    ErrorResponse,
    PostResponse,
    PutResponse,
    DestroyResponse
)



class ObjectCategoryAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        object_category = ObjectCategory.objects.annotate(
            category_count=Count('objectsubcategory'),
            has_data=Case(
                When(category_count__gt=0, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        serializer = ObjectCategorySerializer(object_category, many=True)
        return ListResponse(message="Asosiy buttonlar", data=serializer.data)

object_category_api_view = ObjectCategoryAPIView.as_view()



class ObjectSubCategoryAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            btns = (
                ObjectSubCategory.objects.filter(object_category_id=pk)
                .select_related('object_category')
                .annotate(
                    subcategory_count=Count('object_category', distinct=True),
                    has_data=Case(
                        When(subcategory_count__gt=0, then=Value(True)),
                        default=Value(False),
                        output_field=BooleanField()
                    )
                )
            )

            serializer = ObjectSubCategorySerializer(btns, many=True)
            return ListResponse(data=serializer.data, message="Kategoriya buttonlar")

        except Exception as e:
            return ErrorResponse(message=f"Xatolik yuz berdi: {str(e)}", status_code=500)

    def post(self, request):
        serializer = ObjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return PostResponse(data=serializer.data, message="SubCategory")
        return ErrorResponse(message="Xatolik yuz berdi", errors=serializer.errors, status_code=400)

object_subcategory_button_api_view = ObjectSubCategoryAPIView.as_view()



class ObjectAPIView(APIView):
    # permission_classes = [IsAuthenticated]  

    def get(self, request, pk=None):
        sub_btns = Object.objects.filter(object_subcategory_id=pk).select_related('object_subcategory')
        serializer = ObjectSerializer(sub_btns, many=True)
        return ListResponse(data=serializer.data, message="SubCategory buttonlar")

object_api_view = ObjectAPIView.as_view()
