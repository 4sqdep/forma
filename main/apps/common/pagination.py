from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'page_count': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


# from rest_framework import pagination
# from rest_framework import serializers



# class CustomPagination(pagination.LimitOffsetPagination):
#     default_limit = 5
#     max_limit = 9999999999999999999999
#     min_limit = 1

#     def paginate_queryset(self, queryset, request, view=None):
#         limit = int(request.query_params.get('limit', self.default_limit))
#         page = request.query_params.get('page')

#         if page:
#             page = int(page)
#             if page < 1:
#                 raise serializers.ValidationError(
#                     {"page": ["Page number must be greater than or equal to 1."]}
#                 )
#             offset = (page - 1) * limit
#         else:
#             offset = int(request.query_params.get('offset', 0))

#         if limit > self.max_limit:
#             raise serializers.ValidationError(
#                 {"limit": ["Limit should be less than or equal to {0}".format(self.max_limit)]}
#             )
#         elif limit < self.min_limit:
#             raise serializers.ValidationError(
#                 {"limit": ["Limit should be greater than or equal to {0}".format(self.min_limit)]}
#             )

#         if offset < 0:
#             raise serializers.ValidationError(
#                 {"offset": ["Offset should be greater than or equal to 0."]}
#             )

#         self.limit = limit
#         self.offset = offset
#         return super().paginate_queryset(queryset, request, view)

