from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class SensorFailConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            'fault_log', self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'fault_log', self.channel_name
        )

    def receive(self, text_data):
        self.send(text_data)

    def send_fault_log(self, fault_data):
        self.send(fault_data)
