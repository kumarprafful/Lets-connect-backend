from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Contacts
from users.serializers import ContactSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def fetch_contact_list(request):
    try:
        user = request.user
        contacts = Contacts.objects.get(user=request.user)
        serializer = ContactSerializer(contacts)
        return Response({'status':'success', 'data': serializer.data})
    except Exception as e:
        return Response({'status':'error', 'message':str(e)})
