import ast
import os
import django
import paho.mqtt.client as mqtt
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pinewatchers.settings")
django.setup()
from robots.tasks import (      # noqa: E402
    process_location,
    process_telemetry,
    process_fault
)


def on_connect(client, *args):
    client.subscribe("sensor/#")


def on_message(client, userdata, msg):
    aux_topic = msg.topic.split("/")
    aux_payload = ast.literal_eval(msg.payload.decode("ascii"))
    sensor_name = aux_topic[1]
    message_topic = aux_topic[2]

    if message_topic == "location":
        process_location.delay(sensor_name, aux_payload)
    elif message_topic == "telemetry":
        process_telemetry.delay(sensor_name, aux_payload)
    elif message_topic == "fault_log":
        process_fault.delay(sensor_name, aux_payload)
    else:
        raise NotImplementedError("Unsupported message type.")


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(
        username=settings.MQTT["LOGIN"], password=settings.MQTT["PASSWORD"]
    )
    client.connect(settings.MQTT["HOST"], settings.MQTT["PORT"], 60)
    client.loop_forever()
