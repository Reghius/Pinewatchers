from django.contrib import admin
from .models import Client, RobotManufacturer, RobotType, CommunicationDevice, Robot, Location, Telemetry


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ['KRS_number', 'name']
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
    search_fields = ['name', 'country_of_origin', 'hq_location',]
    list_filter = ('country_of_origin',)
    list_display = (
        'name',
        'country_of_origin',
        'hq_location',
    )


@admin.register(CommunicationDevice)
class CommunicationDeviceAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_filter = ('name',)
    list_display = (
        'name',
        'x_size',
        'y_size',
        'z_size'
    )


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    search_fields = ['name', 'serial_number', 'production_date', 'communication_device']
    list_filter = ('owner', 'manufacturer', 'type')
    list_display = (
        'name',
        'owner',
        'manufacturer',
        'serial_number',
        'production_date',
        'type',
        'communication_device'
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ['robot_object', 'communication_device', 'timestamp']
    list_filter = ('robot_object', 'communication_device')
    list_display = (
        'robot_object',
        'communication_device',
        'timestamp',
        'latitude',
        'longitude'
    )


@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    search_fields = ['robot_object', 'communication_device', 'timestamp']
    list_filter = ('robot_object', 'communication_device')
    list_display = (
        'robot_object',
        'communication_device',
        'timestamp',
        'humidity',
        'temperature',
        'pressure'
    )
