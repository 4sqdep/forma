import django_filters
from django.db.models import Q
from main.apps.project_document.models.project_document_type import ProjectDocumentType




class ProjectDocumentTypeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_search')
    is_forma = django_filters.BooleanFilter(field_name='is_forma')
    is_section = django_filters.BooleanFilter(field_name='is_section')
    is_file = django_filters.BooleanFilter(field_name='is_file')
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    new = django_filters.BooleanFilter(method='order_by_newest')
    old = django_filters.BooleanFilter(method='order_by_oldest')

    class Meta:
        model = ProjectDocumentType
        fields = ['is_forma', 'is_section', 'is_file', 'start_date', 'end_date']

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))

    def order_by_newest(self, queryset, name, value):
        if value:
            return queryset.order_by('-created_at')
        return queryset

    def order_by_oldest(self, queryset, name, value):
        if value:
            return queryset.order_by('created_at')
        return queryset