from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Contacts
from chat.serializers import MessageSerializer

User = get_user_model()

class ContactUserSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'full_name', 'last_message',]

    def get_last_message(self, obj):
        user = self.context.get('user')
        print('obj', obj, user)
        return MessageSerializer(obj.last_message(other_user=user)).data

class ContactSerializer(serializers.ModelSerializer):
    contacts = serializers.SerializerMethodField()

    class Meta:
        model = Contacts
        fields = ['user', 'contacts',]

    def get_contacts(self, obj):
        return ContactUserSerializer(obj.contacts, many=True, context={'user':obj.user}).data
