import django_filters
from django.db.models import Q
from main.apps.object_passport.models.object import Object




class ObjectFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_search')
    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')  
    end_date = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')
    
    new = django_filters.BooleanFilter(method='order_by_newest') 
    old = django_filters.BooleanFilter(method='order_by_oldest')
    expensive = django_filters.BooleanFilter(method='order_by_expensive')
    cheap = django_filters.BooleanFilter(method='order_by_cheap')
    high_energy = django_filters.BooleanFilter(method='order_by_high_energy')
    low_energy = django_filters.BooleanFilter(method='order_by_low_energy')

    class Meta:
        model = Object
        fields = ['start_date', 'end_date']

    def filter_by_search(self, queryset, value):
        return queryset.filter(Q(title__icontains=value))

    def order_by_newest(self, queryset, value):
        if value:
            return queryset.order_by('-created_at')
        return queryset

    def order_by_oldest(self, queryset, value):
        if value:
            return queryset.order_by('created_at')
        return queryset

    def order_by_expensive(self, queryset, value):
        if value:
            return queryset.order_by('-total_price')
        return queryset

    def order_by_cheap(self, queryset, value):
        if value:
            return queryset.order_by('total_price')
        return queryset

    def order_by_high_energy(self, queryset, value):
        if value:
            return queryset.order_by('-object_power')
        return queryset

    def order_by_low_energy(self, queryset, value):
        if value:
            return queryset.order_by('object_power')
        return queryset
