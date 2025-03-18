from django_filters import rest_framework as filters
from core.models import Event

class EventFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    location = filters.CharFilter(lookup_expr='icontains')
    create_date_gte = filters.DateTimeFilter(field_name='create_date', lookup_expr='gte')
    create_date_lte = filters.DateTimeFilter(field_name='create_date', lookup_expr='lte')

    class Meta:
        model = Event
        fields = ['title', 'location', 'create_date_gte', 'create_date_lte']