from django_filters import rest_framework as filters
from robots.models import Location, Telemetry


class LocationFilter(filters.FilterSet):
    class Meta:
        model = Location
        fields = {
            'robot': ['exact'],
            'timestamp': ['gte', 'lte'],
        }

class TelemetryFilter(filters.FilterSet):
    class Meta:
        model = Telemetry
        fields = {
            'robot': ['exact'],
            'timestamp': ['gte', 'lte'],
        }
