import django_filters
from robots.models import Location


class LocationFilter(django_filters.FilterSet):
    class Meta:
        model = Location
        fields = {
            'robot': ['exact'],
            'timestamp': ['timestamp__gte', 'timestamp__lte'],
        }