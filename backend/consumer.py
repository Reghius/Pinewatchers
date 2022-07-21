import paho.mqtt.client as mqtt
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pinewatchers.settings')
django.setup()


def on_connect(client):
    client.subscribe('sensor/#')


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username=os.environ.get('MQTT_LOGIN'), password=os.environ.get('MQTT_PASSWORD'))
client.connect(os.environ.get('MQTT_IP'), os.environ.get('MQTT_PORT'))
client.loop_forever()
