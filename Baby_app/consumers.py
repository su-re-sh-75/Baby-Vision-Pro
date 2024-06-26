from channels.generic.websocket import AsyncWebsocketConsumer
import json
class DashboardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("websocket connection")
        await self.accept()
        # return await super().connect()

    async def disconnect(self, code):
        print(f"websocket connection closed: {code}")
        # return await super().disconnect(code)
        

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        print(message, sender)

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
        # return await super().receive(text_data, bytes_data)