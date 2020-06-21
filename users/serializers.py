from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from chat.serializers import MessageSerializer
from users.models import Contacts, Invites

User = get_user_model()

class ContactUserSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    room_id  = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'room_id', 'last_message',]

    def get_last_message(self, obj):
        user = self.context.get('user')
        return MessageSerializer(obj.last_message(other_user=user)).data

    def get_room_id(self, obj):
        user = self.context.get('user')
        return obj.get_room_id(other_user=user)
class ContactSerializer(serializers.ModelSerializer):
    contacts = serializers.SerializerMethodField()

    class Meta:
        model = Contacts
        fields = ['user', 'contacts',]

    def get_contacts(self, obj):
        return ContactUserSerializer(obj.contacts, many=True, context={'user':obj.user}).data

class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField(source='key')
    key = serializers.CharField(write_only=True)
    ask = serializers.SerializerMethodField(read_only=True)

    def get_ask(self, data):
        first_name = Token.objects.get(key=data.get('key')).user
        if first_name:
            return False
        else:
            return True


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()
    class Meta:
        model = User
        fields = '__all__'

class InvitesSerializer(serializers.ModelSerializer):
    invited_by = UserSerializer()
    class Meta:
        model = Invites
        fields = '__all__'
