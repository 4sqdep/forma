import django_filters
from django.db.models import Q
from main.apps.construction_work.models.file import ConstructionInstallationFile




class ConstructionInstallationFileFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_search')
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')  
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = ConstructionInstallationFile
        fields = ['start_date', 'end_date']

    def filter_by_search(self, queryset, name, value):
        print(f"Search filter hit: {value}")
        return queryset.filter(
            Q(title__icontains=value) | Q(file_code__icontains=value)
        )
