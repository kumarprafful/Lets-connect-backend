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
        self.room = None
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('received', event)
        await self.fetch_user_from_token(event)
        print('--'*100)
        print(self.scope)
        contact_id = json.loads(event.get('text')).get('contact')

        if contact_id:
            self.room = await self.get_room(contact_id)
            pass

        if self.room:
            print("room wala",event)
            
    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @database_sync_to_async
    def fetch_user_from_token(self, event):
        if self.scope['user'].id:
            pass
        else:
            try:
                # It means user is not authenticated yet.
                data = json.loads(event.get('text'))
                if 'authorization' in data.keys():
                    token = data['authorization']
                    token = Token.objects.get(key=token)
                    self.scope['user'] = token.user
                    return
                    
            except Exception as e:
                # Data is not valid, so close it.
                print(e)
                pass

    @database_sync_to_async
    def get_room(self, contact_id):
        print('contact_id', contact_id)
        contact = User.objects.get(id=contact_id)
        print('---'*50)
        print('contact obj',contact)
        room, created = Room.objects.get_or_new(
            first_user=self.scope.get('user'),
            second_user=contact
        )
        print(room, created)
        return room


