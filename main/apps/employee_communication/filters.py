import django_filters
from main.apps.employee_communication.models import EmployeeCommunication
from main.apps.object_passport.models.object import Object




class EmployeeCommunicationFilter(django_filters.FilterSet):
    section_type = django_filters.CharFilter(field_name='section_type', lookup_expr='iexact')
    obj = django_filters.ModelChoiceFilter(queryset=Object.objects.all(), field_name='obj')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    search = django_filters.CharFilter(method='filter_by_search')
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    new = django_filters.BooleanFilter(method='order_by_newest') 
    old = django_filters.BooleanFilter(method='order_by_oldest')

    class Meta:
        model = EmployeeCommunication
        fields = (
            'status', 
            'section_type', 
            'start_date', 
            'end_date', 
            'new', 
            'old'
        )

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(title__icontains=value)

    def order_by_newest(self, queryset, name, value):
        if value:
            return queryset.order_by('-created_at')
        return queryset

    def order_by_oldest(self, queryset, name, value):
        if value:
            return queryset.order_by('created_at')
        return queryset
