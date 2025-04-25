import django_filters
from main.apps.project_document.models.project_file import ProjectDocumentFile
from django.db.models import Q





class ProjectDocumentFileFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_search')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    file_code = django_filters.CharFilter(field_name='file_code', lookup_expr='icontains')
    project_section = django_filters.NumberFilter(field_name='project_section')
    start_date = django_filters.DateFilter(field_name='calendar', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='calendar', lookup_expr='lte')
    new = django_filters.BooleanFilter(method='order_by_newest')
    old = django_filters.BooleanFilter(method='order_by_oldest')

    class Meta:
        model = ProjectDocumentFile
        fields = ['project_section', 'name', 'file_code', 'start_date', 'end_date', 'search']

    
    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(file_code__icontains=value)
        )
    
    def order_by_newest(self, queryset, name, value):
        if value:
            return queryset.order_by('-created_at')
        return queryset

    def order_by_oldest(self, queryset, name, value):
        if value:
            return queryset.order_by('created_at')
        return queryset

