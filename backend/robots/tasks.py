from time import time
from robots.models import Telemetry, Location, CommunicationDevice
import textwrap
from datetime import datetime
import struct
from celery import shared_task


@shared_task
def process_location(sensor_name, location_str):
    seperated_location = textwrap.wrap(location_str, 16)
    timestamp = datetime.fromtimestamp(struct.unpack('>d', bytearray.fromhex(seperated_location[0])))
    latitude = struct.unpack('>d', bytearray.fromhex(seperated_location[1]))
    longitude = struct.unpack('>d', bytearray.fromhex(seperated_location[2]))
    sensor = CommunicationDevice.objects.get(name=sensor_name)

    Location.objects.create(
        communication_device = sensor,
        timestamp = timestamp,
        latitude = latitude,
        longitude = longitude
    )


@shared_task
def process_telemetry(sensor_name, telemetry_str):
    timestamp = datetime.fromtimestamp(struct.unpack('>d', bytearray.fromhex(telemetry_str[:16]))[0])
    humidity = int(telemetry_str[16:18], 16)
    temperature = int(telemetry_str[18:20], 16)
    pressure = int(telemetry_str[20:24], 16)
    sensor = CommunicationDevice.objects.get(name=sensor_name)

    Telemetry.objects.create(
        communication_device = sensor,
        timestamp=timestamp,
        humidity=humidity,
        temperature=temperature,
        pressure=pressure
    )