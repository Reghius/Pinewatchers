import json
from channels.generic.websocket import AsyncWebsocketConsumer


class SensorFailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "fault_log"
        # self.channel_name = "fault_log"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["info"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "fault_log",
                "info": message
            }
        )

    async def fault_log(self, event):
        message = event["message"]
        sensor = event["sensor"]

        await self.send(text_data=json.dumps({
            "info": message,
            "sensor": sensor
        }))
