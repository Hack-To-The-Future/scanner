from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class InferenceConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = "inference_server"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'prediction',
                'json': text_data
            }
        )

    # Receive message from room group
    def prediction(self, event):
        # Send message to WebSocket
        self.send(text_data=event['json'])
