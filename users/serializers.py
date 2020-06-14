from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Contacts

User = get_user_model()

class ContactUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name',]


class ContactSerializer(serializers.ModelSerializer):
    contacts = ContactUserSerializer(many=True)

    class Meta:
        model = Contacts
        fields = ['contacts']