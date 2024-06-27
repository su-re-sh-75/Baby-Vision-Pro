from channels.generic.websocket import AsyncWebsocketConsumer
import json
class DashboardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("websocket connection")
        await self.accept()

    async def disconnect(self, code):
        print(f"websocket connection closed: {code}")
        

    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        await self.send(text_data=json.dumps({
            'message': 'Message received',
        }))