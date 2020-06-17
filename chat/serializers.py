from rest_framework import serializers
from chat.models import Message, Room

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'message', 'created_at']

class RoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(source='get_initial_messages', many=True)
    class Meta:
        model = Room
        fields = ['id', 'messages']