from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Contacts
from users.serializers import ContactSerializer, UserSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def fetch_contact_list(request):
    try:
        user = request.user
        contacts = Contacts.objects.get(user=request.user)
        serializer = ContactSerializer(contacts)
        return Response({'status':'success', 'data': serializer.data}, status=200)
    except Exception as e:
        return Response({'status':'error', 'message':str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def update_customer_info(request):
    try:
        user = request.user
        data = JSONParser().parse(request)
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'status':'error', 'message': serializer.errors}, status=400)
        return Response({'status':'success'}, status=200)
    except Exception as e:
        return Response({'status':'error', 'message':str(e)}, status=400)

