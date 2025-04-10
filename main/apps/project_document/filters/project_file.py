import django_filters
from main.apps.project_document.models.project_file import ProjectDocumentFile




class ProjectDocumentFileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    file_code = django_filters.CharFilter(field_name='file_code', lookup_expr='icontains')
    project_section = django_filters.NumberFilter(field_name='project_section')
    start_date = django_filters.DateFilter(field_name='calendar', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='calendar', lookup_expr='lte')

    class Meta:
        model = ProjectDocumentFile
        fields = ['project_section', 'name', 'file_code', 'start_date', 'end_date']
