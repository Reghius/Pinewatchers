import struct
import textwrap
from datetime import datetime

from celery import shared_task
from channels.layers import get_channel_layer
from django.core.exceptions import FieldError, ObjectDoesNotExist
from robots.models import Location, Robot, Telemetry
from asgiref.sync import async_to_sync


@shared_task
def process_location(sensor_name, data_dict):
    location_str = data_dict["data"]
    seperated_location = textwrap.wrap(location_str, 16)
    timestamp = datetime.fromtimestamp(
        struct.unpack(">d", bytearray.fromhex(seperated_location[0]))[0]
    )
    latitude = struct.unpack(">d", bytearray.fromhex(seperated_location[1]))[0]
    longitude = struct.unpack(">d", bytearray.fromhex(seperated_location[2]))[
        0
    ]
    try:
        robot = Robot.objects.get(communication_device__name=sensor_name)

        Location.objects.create(
            robot=robot,
            timestamp=timestamp,
            latitude=latitude,
            longitude=longitude,
        )
    except FieldError:
        pass
    except ObjectDoesNotExist:
        pass


@shared_task
def process_telemetry(sensor_name, data_dict):
    telemetry_str = data_dict["data"]
    timestamp = datetime.fromtimestamp(
        struct.unpack(">d", bytearray.fromhex(telemetry_str[:16]))[0]
    )
    humidity = int(telemetry_str[16:18], 16)
    temperature = int(telemetry_str[18:20], 16)
    pressure = int(telemetry_str[20:24], 16)
    try:
        robot = Robot.objects.get(communication_device__name=sensor_name)

        Telemetry.objects.create(
            robot=robot,
            timestamp=timestamp,
            humidity=humidity,
            temperature=temperature,
            pressure=pressure,
        )
    except FieldError:
        pass
    except ObjectDoesNotExist:
        pass


@shared_task
def process_fault(sensor_name, data_dict):
    sensor = sensor_name
    fault = data_dict["info"]
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "fault_log",
        {
            "type": "fault_log",
            "message": fault,
            "sensor": sensor
        }
    )
