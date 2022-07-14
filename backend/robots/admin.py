from django.contrib import admin
from .models import Client, RobotManufacturer, RobotType, CommunicationDevice, Robot, Location, Telemetry


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'KRS_number'
    )


@admin.register(RobotType)
class RobotTypeAdmin(admin.ModelAdmin):
    list_filter = ('robot_type',)
    list_display = ('robot_type',)


@admin.register(RobotManufacturer)
class RobotManufacturerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'country_of_origin',
        'HQ_location',
        'robot_types'
    )


@admin.register(CommunicationDevice)
class CommunicationDeviceAdmin(admin.ModelAdmin):
    list_display = (
        'device_id',
        'device_x_size',
        'device_y_size',
        'device_z_size'
    )


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_select_related = ('client', 'robot_type', 'communication_device_id')
    list_display = (
        'robot_name',
        'robot_owner',
        'robot_manufacturer',
        'robot_serial_number',
        'robot_production_date',
        'robot_type',
        'communication_device_id'
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_select_related = ('robot_name', 'communication_device_id')
    list_display = (
        'robot_name',
        'communication_device_id',
        'timestamp',
        'latitude',
        'longitude'
    )


@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    list_select_related = ('robot_name', 'communication_device_id')
    list_display = (
        'robot_name',
        'communication_device_id',
        'timestamp',
        'humidity',
        'temperature',
        'pressure'
    )
