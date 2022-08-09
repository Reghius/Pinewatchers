from django_filters import rest_framework as filters
from robots.models import Location, Robot, Telemetry


class RobotFilter(filters.FilterSet):
    class Meta:
        model = Robot
        fields = {
            "owner__name": ["contains"],
            "manufacturer__name": ["contains"],
            "type__robot_type": ["contains"],
            "name": ["contains"],
            "serial_number": ["contains"],
            "production_date": ["contains"],
        }


class LocationFilter(filters.FilterSet):
    class Meta:
        model = Location
        fields = {
            "robot": ["exact"],
            "timestamp": ["gte", "lte"],
        }


class TelemetryFilter(filters.FilterSet):
    class Meta:
        model = Telemetry
        fields = {
            "robot": ["exact"],
            "timestamp": ["gte", "lte", "range"],
        }
