from channels.generic.websocket import AsyncWebsocketConsumer


class SensorFailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def disconnect(self, close_code):
        pass
