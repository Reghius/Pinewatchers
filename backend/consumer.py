import os
import django
from django.conf import settings
import paho.mqtt.client as mqtt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pinewatchers.settings')
django.setup()


def on_connect(client, *args):
    client.subscribe('sensor/#')


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=settings.MQTT['LOGIN'], password=settings.MQTT['PASSWORD'])
client.connect(settings.MQTT['HOST'], settings.MQTT['PORT'], 60)
client.loop_forever()
