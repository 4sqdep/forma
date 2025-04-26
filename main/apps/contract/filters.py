import django_filters
from main.apps.contract.models import ContractFile
from django.db.models import Q


class ContractFileFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_search')
    section_id = django_filters.NumberFilter(field_name='section_id')
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    new = django_filters.BooleanFilter(method='order_by_newest')
    old = django_filters.BooleanFilter(method='order_by_oldest')

    class Meta:
        model = ContractFile
        fields = ['section_id', 'start_date', 'end_date', 'search']

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(file_code__icontains=value)
        )

    def order_by_newest(self, queryset, title, value):
        if value:
            return queryset.order_by('-created_at')
        return queryset

    def order_by_oldest(self, queryset, title, value):
        if value:
            return queryset.order_by('created_at')
        return queryset

