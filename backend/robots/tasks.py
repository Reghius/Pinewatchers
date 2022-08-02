from robots.models import Telemetry, Location, CommunicationDevice, Robot
import textwrap
from datetime import datetime
import struct
from django.core.exceptions import FieldError, ObjectDoesNotExist
from celery import shared_task


@shared_task
def process_location(sensor_name, location_str):
    seperated_location = textwrap.wrap(location_str, 16)
    timestamp = datetime.fromtimestamp(struct.unpack('>d', bytearray.fromhex(seperated_location[0]))[0])
    latitude = struct.unpack('>d', bytearray.fromhex(seperated_location[1]))[0]
    longitude = struct.unpack('>d', bytearray.fromhex(seperated_location[2]))[0]
    try:
        robot = Robot.objects.get(communication_device__name=sensor_name)

        Location.objects.create(
        robot_name = robot,
        timestamp = timestamp,
        latitude = latitude,
        longitude = longitude
    )
    except FieldError:
        pass
    except ObjectDoesNotExist:
        pass

@shared_task
def process_telemetry(sensor_name, telemetry_str):
    timestamp = datetime.fromtimestamp(struct.unpack('>d', bytearray.fromhex(telemetry_str[:16]))[0])
    humidity = int(telemetry_str[16:18], 16)
    temperature = int(telemetry_str[18:20], 16)
    pressure = int(telemetry_str[20:24], 16)
    try:
        robot = Robot.objects.get(communication_device__name=sensor_name)

        Telemetry.objects.create(
        robot_name = robot,
        timestamp=timestamp,
        humidity=humidity,
        temperature=temperature,
        pressure=pressure
    )
    except FieldError:
        pass
    except ObjectDoesNotExist:
        pass
