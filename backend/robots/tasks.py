from time import time
from robots.models import Telemetry, Location, Robot, CommunicationDevice
import textwrap
from datetime import datetime
import struct
from celery import shared_task


@shared_task
def process_location(robot_name, sensor_nr, location_str):
    seperated_location = textwrap.wrap(location_str, 16)
    timestamp = datetime.fromtimestamp(struct.unpack('>d', bytearray.fromhex(seperated_location[0])))
    latitude = struct.unpack('>d', bytearray.fromhex(seperated_location[1]))
    longitude = struct.unpack('>d', bytearray.fromhex(seperated_location[2]))
    robot = Robot.objects.get(name=robot_name)
    sensor = CommunicationDevice.objects.get(name=sensor_nr)

    Location.objects.create(
        robot_object = robot,
        communication_device = sensor,
        timestamp = timestamp,
        latitude = latitude,
        longitude = longitude
    )


@shared_task
def process_telemetry():
    pass
