import django_filters
from django.utils.dateparse import parse_date
from main.apps.construction_work.models.section import ConstructionInstallationSection




class ConstructionInstallationSectionFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_search')
    is_forma = django_filters.BooleanFilter(field_name='is_forma')
    is_file = django_filters.BooleanFilter(field_name='is_file')
    start_date = django_filters.DateFilter(method='filter_start_date')
    end_date = django_filters.DateFilter(method='filter_end_date')
    new = django_filters.BooleanFilter(method='filter_newest')
    old = django_filters.BooleanFilter(method='filter_oldest')

    class Meta:
        model = ConstructionInstallationSection
        fields = ['is_forma', 'is_file', 'start_date', 'end_date']

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(title__icontains=value)

    def filter_start_date(self, queryset, name, value):
        date = parse_date(str(value))
        if date:
            return queryset.filter(created_at__date__gte=date)
        return queryset

    def filter_end_date(self, queryset, name, value):
        date = parse_date(str(value))
        if date:
            return queryset.filter(created_at__date__lte=date)
        return queryset

    def filter_newest(self, queryset, name, value):
        if value:
            return queryset.order_by('-created_at')
        return queryset

    def filter_oldest(self, queryset, name, value):
        if value:
            return queryset.order_by('created_at')
        return queryset
