from django.contrib import admin

from .models import (
    Client,
    CommunicationDevice,
    Location,
    Robot,
    RobotManufacturer,
    RobotModificationHistory,
    RobotType,
    Telemetry,
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ["krs_number", "name"]
    list_filter = ("krs_number", "name")
    list_display = ("name", "krs_number")


@admin.register(RobotType)
class RobotTypeAdmin(admin.ModelAdmin):
    list_display = ("robot_type",)


@admin.register(RobotManufacturer)
class RobotManufacturerAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "country_of_origin",
        "hq_location",
    ]
    list_filter = ("country_of_origin",)
    list_display = (
        "name",
        "country_of_origin",
        "hq_location",
    )


@admin.register(CommunicationDevice)
class CommunicationDeviceAdmin(admin.ModelAdmin):
    search_fields = ["name", "robot"]
    list_filter = ("name", "robot")
    list_display = ("name", "x_size", "y_size", "z_size", "robot")


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    search_fields = ["name", "serial_number", "production_date"]
    list_filter = ("owner", "manufacturer", "type")
    list_display = (
        "name",
        "owner",
        "manufacturer",
        "serial_number",
        "production_date",
        "type",
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ["robot", "timestamp"]
    list_filter = ("robot",)
    list_display = ("robot", "timestamp", "latitude", "longitude")


@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    search_fields = ["robot", "timestamp"]
    list_filter = ("robot",)
    list_display = (
        "robot",
        "timestamp",
        "humidity",
        "temperature",
        "pressure",
    )


@admin.register(RobotModificationHistory)
class RobotModificationHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "manufacturer",
        "serial_number",
        "production_date",
        "type",
        "modification_date"
    )
