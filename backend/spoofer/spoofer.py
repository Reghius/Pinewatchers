import paho.mqtt.client as mqtt
import time
from datetime import datetime, timezone
import struct
import binascii
import random
import os
import logging


logger = logging.getLogger(__name__)

NUM_OF_SENSORS = int(os.getenv("NUM_OF_SENSORS", 20))
SLEEP_TIME = float(os.getenv("SPOOF_SLEEP_TIME", 0.05))
FAULT_CHANCE = float(os.getenv("SENSOR_FAULT_CHANCE", 0.1))
FAULT_RECOVERY_CHANCE = float(os.getenv("SENSOR_FAULT_RECOVERY_CHANCE", 5))


def _double_to_hex(double):
    return str(binascii.hexlify(struct.pack(">d", double)), encoding="utf-8")


def _get_log_packet() -> str:
    timestamp_str = _double_to_hex(
        datetime.now().replace(tzinfo=timezone.utc).timestamp()
    )
    humidity_str = hex(random.randint(30, 90))[2:]
    temperature_str = hex(random.randint(10, 40))[2:]
    pressure_str = hex(random.randint(950, 1050))[2:].zfill(4)

    return (
        timestamp_str + humidity_str + temperature_str + pressure_str
    ).upper()


def _get_location_packet() -> str:
    timestamp_str = _double_to_hex(
        datetime.now().replace(tzinfo=timezone.utc).timestamp()
    )
    latitude = _double_to_hex(
        50.656971 + (random.random() - 0.5) / 1000
    ).zfill(16)
    longitude = _double_to_hex(
        17.867373 + (random.random() - 0.5) / 1000
    ).zfill(16)

    return (timestamp_str + latitude + longitude).upper()


def print_col(color: str, text: str) -> str:
    return f"\033[{color}m{text}\033[0m"


def handle_faults(sensor_nr: int, faulty_sensors: set) -> None:
    """
    Simulates a chance of a sensor fault and recovery.
    """
    if random.random() * 100 < FAULT_CHANCE:
        faulty_sensors.add(sensor_nr)
        client.publish(
            f"sensor/{sensor_nr}/fault_log",
            payload=str({"info": "fault_detected"}),
        )
        logger.info(
            f'{print_col("91", "[!]")} "{sensor_nr}" '
            '>>> spoofed sensor failure'
        )
    elif random.random() * 100 < FAULT_RECOVERY_CHANCE:
        faulty_sensors.remove(sensor_nr)
        client.publish(
            f"sensor/{sensor_nr}/fault_log",
            payload=str({"info": "fault_recovered"}),
        )
        logger.info(
            f'{print_col("91", "[!]")} "{sensor_nr}" '
            '>>> spoofed sensor failure recovery.'
        )


def handle_data_spoofing(sensor_nr: int, faulty_sensors: set) -> None:
    """
    Spoofs sensor data.
    """

    if len(faulty_sensors) == NUM_OF_SENSORS:
        logger.warning(
            f'{print_col("93", "[?]")} No working sensors found, '
            f"cannot spoof data, sleeping for {SLEEP_TIME:.2f}s"
        )
        return

    is_log_packet = random.randint(0, 1)
    data = _get_log_packet() if is_log_packet else _get_location_packet()

    client.publish(
        f"sensor/{sensor_nr}/"
        f"{'telemetry' if is_log_packet else 'location'}",
        payload=str({"data": data}),
    )

    logger.info(
        f'{print_col("92", "[+]")} "{sensor_nr}" >>> spoofed '
        f"sensor data, sleeping for {SLEEP_TIME:.2f}s"
    )


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("sensor-broker", 1883, 60)
    faulty_sensors = set()

    while True:
        sensor_nr = f'SNR{str(random.randint(1, NUM_OF_SENSORS)).zfill(2)}'
        while sensor_nr in faulty_sensors:
            sensor_nr = f'SNR{str(random.randint(1, NUM_OF_SENSORS)).zfill(2)}'

        handle_faults(sensor_nr, faulty_sensors)
        handle_data_spoofing(sensor_nr, faulty_sensors)
        time.sleep(SLEEP_TIME)
