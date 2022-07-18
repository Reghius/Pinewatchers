from django.contrib import admin
from .models import Client, RobotManufacturer, RobotType, CommunicationDevice, Robot, Location, Telemetry


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_filter = ('KRS_number', 'name')
    list_display = (
        'name',
        'KRS_number'
    )


@admin.register(RobotType)
class RobotTypeAdmin(admin.ModelAdmin):
    list_display = ('robot_type',)


@admin.register(RobotManufacturer)
class RobotManufacturerAdmin(admin.ModelAdmin):
    list_filter = ('country_of_origin',)
    list_display = (
        'name',
        'country_of_origin',
        'HQ_location',
    )


@admin.register(CommunicationDevice)
class CommunicationDeviceAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = (
        'name',
        'x_size',
        'y_size',
        'z_size'
    )


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_filter = ('owner', 'manufacturer', 'type')
    list_display = (
        'name',
        'owner',
        'manufacturer',
        'serial_number',
        'production_date',
        'type',
        'communication_device_name'
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_filter = ('robot_object', 'communication_device_name')
    list_display = (
        'robot_object',
        'communication_device_name',
        'timestamp',
        'latitude',
        'longitude'
    )


@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    list_filter = ('robot_object', 'communication_device_name')
    list_display = (
        'robot_object',
        'communication_device_name',
        'timestamp',
        'humidity',
        'temperature',
        'pressure'
    )
