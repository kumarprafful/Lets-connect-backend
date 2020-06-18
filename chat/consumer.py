import json

from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from chat.models import Room, Message

User = get_user_model()

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        self.pre_rooms = None
        self.rooms = set()
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('received', event)
        await self.fetch_user_from_token(event)
        pre_rooms = self.pre_rooms
        if pre_rooms:
            for room in pre_rooms:
                self.rooms.add(f'room_{str(room)}')
                await self.channel_layer.group_add(
                    f'room_{str(room)}',
                    self.channel_name,
                )
            self.pre_rooms = None

        message = json.loads(event.get('text')).get('message')
        if message:
            msg = await self.create_msg(message.get('roomID'), message.get('msg'))

            myResponse = {
                'roomID': str(msg.room.id),
                'messageObj':{
                    'sender': str(msg.sender.id),
                    'message': msg.message,
                    'created_at': str(msg.created_at),
                }
            }

            await self.channel_layer.group_send(
                f'room_{message.get("roomID")}',
                {
                    'type': 'chat_message',
                    'text': json.dumps(myResponse)
                }
            )
    
    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })


    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @database_sync_to_async
    def fetch_user_from_token(self, event):
        if self.scope['user'].id:
            return
        else:
            try:
                # It means user is not authenticated yet.
                data = json.loads(event.get('text'))
                if 'authorization' in data.keys():
                    token = data['authorization']
                    token = Token.objects.get(key=token)
                    self.scope['user'] = token.user
                    self.pre_rooms = token.user.get_rooms()
                    return
                    
            except Exception as e:
                # Data is not valid, so close it.
                print('EXCEPTION ====> ',e)
                pass


    @database_sync_to_async
    def create_msg(self, room_id, message):
        print(self.scope.get('user'))
        room = Room.objects.get(id=room_id)
        return Message.objects.create(
            room=room,
            message=message,
            sender=self.scope.get('user'),
        )

    